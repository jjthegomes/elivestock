import express from "express";
import Alimento from "../models/alimento";
import ProdLeiteGeral from "../models/prodleiteGeral";
import { createObjectCsvWriter } from "csv-writer";

const router = express.Router();

router.get("/", async (req, res) => {
  try {
    const list = await Alimento.find();
    return res.send(list).status(200);
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/", async (req, res) => {
  const { alimentos } = req.body;

  if (!Array.isArray(alimentos)) {
    const alimento = await Alimento.create(JSON.parse(alimentos));
    await alimento.save();
    return res.status(200).send({ alimentos });
  }

  try {
    await Promise.all(
      alimentos.map(async (current) => {
        let item = JSON.parse(current);

        let alimento = await Alimento.create(item);
        await alimento.save();
        return;
      })
    );

    return res.status(200).send({ alimentos });
  } catch (error) {
    res.status(400).send({ error: "erro!" });
    console.log(error);
  }
});

router.post("/buscar/lote", async (req, res) => {
  const { date, lote } = req.body;
  try {
    let alimento = null;
    if (date != undefined) {
      alimento = await Alimento.find({ lote: lote, date: date });
    } else {
      alimento = await Alimento.find({ lote });
    }

    return res.status(200).send({ alimento });
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

router.post("/consolidated", async (req, res) => {
  const { lote } = req.body;
  try {
    let alimentos = await Alimento.aggregate([
      { $match: { lote: lote } },
      {
        $group: {
          _id: "$alimento",
          total: { $sum: "$totalLote" },
          avgNumAnimais: { $avg: "$numAnimais" },
          avgMediaVacaDia: { $avg: "$mediaVaca" },
        },
      },
    ]);

    let consolidated = [];
    for (let item of alimentos) {
      let mediaTotalVaca = 0;
      if (item.total > 0)
        mediaTotalVaca = Number((item.total / item.avgNumAnimais).toFixed());
      consolidated.push({ ...item, mediaTotalVaca });
    }

    return res.status(200).send(consolidated);
  } catch (error) {
    res.status(400).send({ error: "erro consolidated!" });
  }
});

router.get("/leiteGeral", async (req, res) => {
  try {
    const listAlimento = await Alimento.find({
      $or: [{ lote: 1 }, { lote: 2 }, { lote: 3 }],
    });
    const listLeiteGeral = await ProdLeiteGeral.find();

    let newList = listAlimento.map((item) => ({
      lote: item.lote,
      date: item.date.split(" ")[0],
      qtd_animais: item.numAnimais,
      alimento: item.alimento,
      totalLote: item.totalLote,
    }));

    let experiment = [];
    for (const item of newList) {
      let el = listLeiteGeral.find(
        (prod) => prod.date === item.date && prod.lote == item.lote
      );
      if (el) {
        experiment.push({
          lote: item.lote,
          date: item.date,
          producao: el.producao,
          alimento: item.alimento,
          totalLote: item.totalLote,
          qtd_animais_alimentados: item.qtd_animais,
        });
      }
    }

    let lote1 = experiment.filter((e) => e.lote === "1");
    let lote2 = experiment.filter((e) => e.lote === "2");
    let lote3 = experiment.filter((e) => e.lote === "3");

    // let fileName = 'alimentoXleite.csv';
    // const csvWriter = createObjectCsvWriter({
    //   path: "csv/" + fileName,
    //   header: [
    //     { id: 'lote', title: 'lote' },
    //     { id: 'date', title: 'date' },
    //     { id: 'producao', title: 'producao. Leite' },
    //     { id: 'alimento', title: 'alimento' },
    //     { id: 'totalLote', title: 'totalLote' },
    //     { id: 'qtd_animais_alimentados', title: 'qtd_animais_alimentados' },
    //   ]
    // });

    // try {
    //   await csvWriter.writeRecords(experiment)
    //   console.log('The CSV file was written successfully')
    // } catch (error) {
    //   console.log('The CSV file was NOT written!')
    // }

    return res.status(200).send({ lote1, lote2, lote3 });
    // return res.status(200).send(experiment)
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.get("/tipo", async (req, res) => {
  try {
    const listAlimento = await Alimento.find({
      $or: [{ lote: 1 }, { lote: 2 }, { lote: 3 }],
    });
    const listLeiteGeral = await ProdLeiteGeral.find();

    let newList = listAlimento.map((item) => ({
      lote: item.lote,
      date: item.date.split(" ")[0],
      qtd_animais: item.numAnimais,
      alimento: item.alimento,
      totalLote: item.totalLote,
    }));

    let experiment = [];
    for (const item of newList) {
      let el = listLeiteGeral.find(
        (prod) => prod.date === item.date && prod.lote == item.lote
      );
      if (el) {
        experiment.push({
          lote: item.lote,
          date: item.date,
          producao: el.producao,
          alimento: item.alimento,
          totalLote: item.totalLote,
          qtd_animais_alimentados: item.qtd_animais,
        });
      }
    }

    const tipos = await Alimento.distinct("alimento");
    // let tipos = [
    //   "Algodão",
    //   "CONCENTRADO",
    //   "Complemento alimenta",
    //   "Farinha de Milho",
    //   "Farinha de Soja",
    //   "Feno",
    //   "Silagem de milho"
    // ]

    let obj = {};
    for (const item of tipos) {
      let el = experiment.filter((e) => e.alimento === item);
      obj = {
        ...obj,
        [item]: el,
      };
    }

    return res.status(200).send({ tipos, data: obj });
    // return res.status(200).send(experiment)
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.get("/tipo/leite", async (req, res) => {
  try {
    const listAlimento = await Alimento.find({
      $or: [{ lote: 1 }, { lote: 2 }, { lote: 3 }],
    });
    const listLeiteGeral = await ProdLeiteGeral.find();

    let newList = listAlimento.map((item) => ({
      lote: item.lote,
      date: item.date.split(" ")[0],
      qtd_animais: item.numAnimais,
      alimento: item.alimento,
      totalLote: item.totalLote,
    }));

    let experiment = [];
    for (const item of newList) {
      let el = listLeiteGeral.find(
        (prod) => prod.date === item.date && prod.lote == item.lote
      );
      if (el) {
        experiment.push({
          lote: item.lote,
          date: item.date,
          producao: el.producao,
          alimento: item.alimento,
          totalLote: item.totalLote,
          qtd_animais_alimentados: item.qtd_animais,
        });
      }
    }

    let dates = [];

    for (const item of experiment) {
      if (!dates.includes(item.date)) dates.push(item.date);
    }

    let obj = {};

    for (const item of dates) {
      let el = experiment.filter((e) => e.date === item);
      obj = {
        ...obj,
        [item]: el,
      };
    }

    let lotes = ["1", "2", "3"];
    // key = 2020-10-30
    //element = { .... }
    let result = {};
    for (const key in obj) {
      let novo_element = [];
      if (Object.hasOwnProperty.call(obj, key)) {
        const element = obj[key];

        let el1 = element.filter((e) => e.lote === "1");
        let el2 = element.filter((e) => e.lote === "3");
        let el3 = element.filter((e) => e.lote === "2");

        let lote1 = {};
        for (const item of el1) {
          lote1 = {
            ...lote1,
            [item.alimento]: item.totalLote,
          };
        }
        let lote2 = {};
        for (const item of el2) {
          lote2 = {
            ...lote2,
            [item.alimento]: item.totalLote,
          };
        }
        let lote3 = {};
        for (const item of el3) {
          lote3 = {
            ...lote3,
            [item.alimento]: item.totalLote,
          };
        }

        novo_element.push({
          lote1,
          lote2,
          lote3,
          leite: element[0].producao,
        });
        result = {
          ...result,
          [key]: novo_element,
        };
      }

      // for (const item of element) {
      //   result.push({
      //     [item.lote]: item.alimento
      //   })
      // }
    }

    return res.status(200).send(result);
    // return res.status(200).send(experiment)
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.get("/csv", async (req, res) => {
  try {
    const listAlimento = await Alimento.find({
      $or: [{ lote: 1 }, { lote: 2 }, { lote: 3 }],
    });
    const listLeiteGeral = await ProdLeiteGeral.find();

    let newList = listAlimento.map((item) => ({
      lote: item.lote,
      date: item.date.split(" ")[0],
      qtd_animais: item.numAnimais,
      alimento: item.alimento,
      totalLote: item.totalLote,
    }));

    let experiment = [];
    for (const item of newList) {
      let el = listLeiteGeral.find(
        (prod) => prod.date === item.date && prod.lote == item.lote
      );
      if (el) {
        experiment.push({
          lote: item.lote,
          date: item.date,
          producao: el.producao,
          alimento: item.alimento,
          totalLote: item.totalLote,
          qtd_animais_alimentados: item.qtd_animais,
        });
      }
    }

    let dates = [];

    for (const item of experiment) {
      if (!dates.includes(item.date)) dates.push(item.date);
    }

    let obj = {};

    for (const item of dates) {
      let el = experiment.filter((e) => e.date === item);
      obj = {
        ...obj,
        [item]: el,
      };
    }

    let lotes = ["1", "2", "3"];
    // key = 2020-10-30
    //element = { .... }
    let result = {};

    let csvData = [];

    for (const key in obj) {
      let novo_element = [];
      if (Object.hasOwnProperty.call(obj, key)) {
        const element = obj[key];

        let el1 = element.filter((e) => e.lote === "1");
        let el2 = element.filter((e) => e.lote === "3");
        let el3 = element.filter((e) => e.lote === "2");

        let lote1 = {};
        for (const item of el1) {
          lote1 = {
            ...lote1,
            [item.alimento]: item.totalLote,
            qtd_animais_alimentados: item.qtd_animais_alimentados,
          };
        }
        let lote2 = {};
        for (const item of el2) {
          lote2 = {
            ...lote2,
            [item.alimento]: item.totalLote,
            qtd_animais_alimentados: item.qtd_animais_alimentados,
          };
        }
        let lote3 = {};
        for (const item of el3) {
          lote3 = {
            ...lote3,
            [item.alimento]: item.totalLote,
            qtd_animais_alimentados: item.qtd_animais_alimentados,
          };
        }

        csvData.push({
          ...lote1,
          lote: "1",
          leite: element[0].producao,
          date: key,
        });

        csvData.push({
          ...lote2,
          lote: "2",
          leite: element[0].producao,
          date: key,
        });

        csvData.push({
          ...lote3,
          lote: "3",
          leite: element[0].producao,
          date: key,
        });

        novo_element.push({
          lote1,
          lote2,
          lote3,
          leite: element[0].producao,
        });
        result = {
          ...result,
          [key]: novo_element,
        };
      }
    }

    let fileName = "alimentoXtipo.csv";
    const csvWriter = createObjectCsvWriter({
      path: "csv/" + fileName,
      header: [
        { id: "date", title: "date" },
        { id: "Algodão", title: "Algodão" },
        { id: "CONCENTRADO", title: "CONCENTRADO" },
        { id: "Complemento alimenta", title: "Complemento alimenta" },
        { id: "Farinha de Milho", title: "Farinha de Milho" },
        { id: "Farinha de Soja", title: "Farinha de Soja" },
        { id: "Feno", title: "Feno" },
        { id: "Silagem de milho", title: "Silagem de milho" },
        { id: "lote", title: "lote" },
        { id: "leite", title: "leite" },
        { id: "qtd_animais_alimentados", title: "qtd_animais_alimentados" },
      ],
    });

    try {
      await csvWriter.writeRecords(csvData);
      console.log("The CSV file was written successfully");
    } catch (error) {
      console.log("The CSV file was NOT written!");
    }
    return res.status(200).send(csvData);
  } catch (error) {
    return res.send("erro").status(500);
  }
});

module.exports = (app) => app.use("/api/alimento", router);
