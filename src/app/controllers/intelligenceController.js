import express from "express";
import axios from "axios";
import Alerta from "../models/alert";
import Intelligence from "../models/intelligence";
import Temperature from "../models/temperature";
import Humidity from "../models/humdity";

const router = express.Router();
const BASE_URL = "http://localhost:5000/api/predict";

router.get("/", async (req, res) => {
  try {
    const response = await axios.get("http://localhost:5000/");
    return res.send({ data: "API online!" }).status(200);
  } catch (error) {
    if (error.message == "Request failed with status code 403")
      return res.send({ error: "API offline!" }).status(500);
    return res.send({ error }).status(500);
  }
});

router.get("/list", async (req, res) => {
  try {
    const list = await Intelligence.find().sort({ active: -1 });
    return res.send(list).status(200);
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/", async (req, res) => {
  try {
    const intel = await Intelligence.create(req.body);
    await intel.save();
    return res.send(intel).status(200);
  } catch (error) {
    return res.send({ error }).status(500);
  }
});

router.post("/leite/geral", async (req, res) => {
  const { date } = req.body;
  if (!date) return res.status(500).send({ error: "Data é necessário" });

  try {
    const response = await axios.post(BASE_URL + "/milk/geral", req.body);
    const { result } = response.data;

    const alerta = await Alerta.create({
      title: "Predição de leite",
      desc: `Para o dia ${date} a previsão produção de leite da fazenda será de ${result}L.`,
      type: "prediction",
    });

    await alerta.save();

    return res.send({ data: req.body, result }).status(200);
  } catch (error) {
    console.log(error);
    return res.status(500).send({ error });
  }
});

router.post("/leite/individual", async (req, res) => {
  const { Peso, date } = req.body;
  if (!Peso && !date)
    return res.status(500).send({ error: "Peso e date (mes) é necessário" });

  try {
    const response = await axios.post(BASE_URL + "/milk/individual", req.body);
    const { result } = response.data;

    const alerta = await Alerta.create({
      title: "Predição de leite",
      desc: `Para animal com peso de ${Peso} no mês ${date}, a produção prevista será de ${result.toFixed(
        2
      )}L.`,
      type: "prediction",
    });
    await alerta.save();

    return res.send({ data: req.body, result }).status(200);
  } catch (error) {
    return res.status(500).send({ error });
  }
});

router.post("/leite/alimento", async (req, res) => {
  try {
    const response = await axios.post(BASE_URL + "/milk/alimento", req.body);
    const { result } = response.data;

    const alerta = await Alerta.create({
      title: "Predição de leite",
      desc: `Para dieta solicitada a produção geral prevista será de ${result.toFixed(
        2
      )}L.
        Farinha de Milho: ${req.body["Farinha de Milho"]}Kg,
        Farinha de Soja: ${req.body["Farinha de Soja"]}Kg,
        Silagem de milho: ${req.body["Silagem de milho"]}Kg,
        Algodão:  ${req.body["Algodão"]}Kg,
        Feno: ${req.body["Feno"]}Kg,
        Complemento alimenta: ${req.body["Complemento alimenta"]}Kg.
        `,
      type: "prediction",
    });
    await alerta.save();

    return res.send({ data: req.body, result }).status(200);
  } catch (error) {
    return res.status(500).send({ error });
  }
});

router.post("/lote/mastite", async (req, res) => {
  try {
    const response = await axios.post(BASE_URL + "/animal/lote/mastite", {});
    return res.send({ data: response.data }).status(200);
  } catch (error) {
    return res.status(500).send({ error });
  }
});

router.post("/lote/leite", async (req, res) => {
  try {
    const response = await axios.post(
      BASE_URL + "/animal/lote/leite",
      req.body
    );

    return res.send({ data: response.data }).status(200);
  } catch (error) {
    return res.status(500).send({ error });
  }
});
router.get("/ambiente/forescast", async (req, res) => {
  try {
    const response = await axios.get(
      "https://apiprevmet3.inmet.gov.br/previsao/3119609"
    );
    const data = response.data["3119609"];

    let dates = [];
    for (const key in data) {
      if (Object.hasOwnProperty.call(data, key)) {
        dates.push(key);
      }
    }

    return res.status(200).send({ dates, data });
  } catch (error) {
    res.status(400).send({ error });
  }
});
router.post("/ambiente/historical", async (req, res) => {
  try {
    const { start_date, end_date, type } = req.body;

    if (!start_date)
      return res
        .status(200)
        .send({ error: "Informe a data - start_date: YYYY-MM-DD" });

    //  TO-DO get local data based on start_date and end_date
    // const listTemperature = await Temperature.find({ source: "inmet"});
    // const listHumidity = await Humidity.find({ source: "inmet" });

    // return res.status(200).send({ listHumidity });

    let request = `https://apitempo.inmet.gov.br/estacao/${start_date}/${start_date}/A557`;

    if (start_date && end_date)
      request = `https://apitempo.inmet.gov.br/estacao/${start_date}/${end_date}/A557`;

    const response = await axios.get(request);
    const data = response.data;

    let listDate = [];

    for (const item of data) {
      if (!listDate.includes(item.DT_MEDICAO)) listDate.push(item.DT_MEDICAO); //lista de datas
    }

    const average = (data, field) =>
      data.reduce(function (sum, item) {
        if (item[field]) {
          return sum + parseFloat(item[field]);
        }
        return sum;
      }, 0) / data.length;

    let list = [];

    if (type && type == "temperature") {
      for (const item of listDate) {
        const temp = data.filter((e) => e.DT_MEDICAO === item);
        const avgTemperature = average(temp, "TEM_INS").toFixed(2);
        list.push({
          date: item,
          temperature: Number(avgTemperature),
        });
      }
    } else if (type && type == "humidity") {
      for (const item of listDate) {
        const temp = data.filter((e) => e.DT_MEDICAO === item);
        const avgHumidity = average(temp, "UMD_INS").toFixed(2);
        list.push({
          date: item,
          humidity: Number(avgHumidity),
        });
      }
    } else {
      for (const item of listDate) {
        const temp = data.filter((e) => e.DT_MEDICAO === item);
        const avgTemperature = average(temp, "TEM_INS").toFixed(2);
        const avgHumidity = average(temp, "UMD_INS").toFixed(2);
        list.push({
          date: item,
          temperature: avgTemperature,
          humidity: avgHumidity,
        });
      }
    }

    return res.status(200).send({ data: list });
  } catch (error) {
    res.status(400).send({ error });
  }
});

module.exports = (app) => app.use("/api/intelligence", router);
