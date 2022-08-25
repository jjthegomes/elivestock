import express from "express";
import CsvReadableStream from "csv-reader";
import { createObjectCsvWriter } from "csv-writer";
import fs from "fs";

import Temperature from "../models/temperature";
import Humidity from "../models/humdity";
import Animal from "../models/animal";
import OnFarm from "../models/onfarm";
import Alimento from "../models/alimento";
import ProdLeite from "../models/prodleite";
import ProdLeiteGeral from "../models/prodleiteGeral";
import Balanca from "../models/balanca";
import { formatNumber, formatDate } from "../../helpers/parser";
import { getAvgValueAmbiente, getPesoLeite } from "../../helpers/utils";
const router = express.Router();

//POST
router.post("/onfarm", async (req, res) => {
  try {
    let inputStream = fs.createReadStream("OnfarmBR.csv", "utf8");

    let OnfarmBR = [
      "REBANHO",
      "ESTADO",
      "SISTEMA",
      "VACAS EM LACTAÇÃO",
      "	TOTAL PROD. LEITE",
      "BRINCO",
      "DATA MASTITE",
      "TETO",
      "	TIPO MASTITE",
      "MC",
      "GRAU",
      "OBS",
      "GRUMO",
      "DIAS TRATAMENTO",
      "PROTOCOLO NOME",
      "ATB INTRAMAMÁRIO 1",
      "DIAS TRATAMENTO ATB INTRAMAMARIO 1",
      "ATB INTRAMAMÁRIO 2",
      "DIAS TRATAMENTO ATB INTRAMAMARIO 2",
      "ATB INJETÁVEL",
      "DIAS TRATAMENTO ATB INJETÁVEL",
      "ANTI-INFLAMATÓRIO",
      "DIAS TRATAMENTO ANTI-INFLAMATÓRIO",
      "CURA CLÍNICA",
      "Nº DE CASOS CLÍNICOS, Nº DE CULTURAS",
      "AGENTE 1",
      "AGENTE 2",
      "AGENTE 3",
      "RESULTADO",
      "POSITIVO",
      "GRAM POS",
      "GRAM NEG",
      "E.COLI",
      "ENTEROCOCCUS SPP",
      "KLEBSIELLA / ENTEROBACTER",
      "LACTOCOCCUS SPP",
      "OUTROS GRAM - NEG",
      "OUTROS GRAM - POS",
      "PROTOTHECA / LEVEDURA",
      "PSEUDOMONAS SPP",
      "SERRATIA SPP",
      "STAPH NÃO AUREUS",
      "STAPH AUREUS",
      "STREP AGALACTIAE / DYSGALACTIAE",
      "STREP UBERIS",
      "ID_ATENDIMENTO",
      "ID_ANIMAL",
      "DESCRICAO_QUARTO",
      "DATA_ATENDIMENTO",
    ];
    inputStream
      .pipe(
        new CsvReadableStream({
          parseNumbers: true,
          delimiter: ";",
          parseBooleans: true,
          trim: true,
        })
      )
      .on("data", async function (row) {
        try {
          // console.log('A row arrived: ', row[0]);
          if (row[0] == OnfarmBR[0]) {
            return;
          }

          const onfarmObj = {
            rebanho: row[0] || "",
            estado_uf: row[1] || "",
            sistema: row[2] || "",
            vacasLactacao: row[3] || "",
            totalProdLeite: row[4] || "",
            brinco: row[5] || "",
            dataMastite: row[6] || "",
            teto: row[7] || "",
            tipoMastite: row[8] || "",
            mc: row[9] || "",
            grau: row[10] || "",
            obs: row[11] || "",
            grumo: row[12] || "",
            diasTratamento: row[13] || "",
            protocoloNome: row[14] || "",
            AtbIntramamario1: row[15] || "",
            diasTratamentoAtbIntramamario1: row[16] || "",
            AtbIntramamario2: row[17] || "",
            diasTratamentoAtbIntramamario2: row[18] || "",
            AtbInjetavel: row[19] || "",
            diasTratamentoAtbInjetavel: row[20] || "",
            antiInflamatorio: row[21] || "",
            diasTratamentoAntiInflamatorio: row[22] || "",
            curaClinica: row[23] || "",
            numCasosClinicos: row[24] || "",
            numCulturas: row[25] || "",
            agente1: row[26] || "",
            agente2: row[27] || "",
            agente3: row[28] || "",
            resultado: row[29] || "",
            positivo: row[30] || "",
            gramPositiva: row[31] || "",
            gramNegativa: row[32] || "",
            E_COLI: row[33] || "",
            ENTEROCOCCUS_SPP: row[34] || "",
            KLEBSIELLA_ENTEROBACTER: row[35] || "",
            LACTOCOCCUS_SPP: row[36] || "",
            outrosGramNegativa: row[37] || "",
            outrosGramPositiva: row[38] || "",
            PROTOTHECA_LEVEDURA: row[39] || "",
            PSEUDOMONAS_SPP: row[40] || "",
            SERRATIA_SPP: row[41] || "",
            STAPH_NAO_AUREUS: row[42] || "",
            STAPH_AUREUS: row[43] || "",
            STREP_AGALACTIAE_DYSGALACTIAE: row[44] || "",
            STREP_UBERIS: row[45] || "",
            idAtendimento: row[46] || "",
            idAnimal: row[47] || "",
            descricaoQuarto: row[48] || "",
            dataAtendimento: row[49] || "",
          };

          // if (onfarmObj['dataAtendimento'] == null)
          //   delete onfarmObj.dataNascimento
          // if (onfarmObj['dataMastite'] == null)
          //   delete onfarmObj.ultimoParto
          // console.log(onfarmObj);
          const onfarm = await OnFarm.create(onfarmObj);
          await onfarm.save();
        } catch (error) {
          console.log("deu ruim", error);
        }
      })
      .on("end", async function (data) {
        // console.log('No more rows!');
        const list = await OnFarm.find();
        return res.send(list).status(200);
      });
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/animal", async (req, res) => {
  try {
    let inputStream = fs.createReadStream(
      "embrapa-gado-de-leite-animal-datatable.csv",
      "utf8"
    );

    let embrapa_gado_de_leite_animal_datatable = [
      "Brinco",
      "Animal",
      "Lote",
      "Status",
      "DEL",
      "DEA",
      "Data de nascimento",
      "Último parto",
      "Última inseminação",
    ];

    inputStream
      .pipe(
        new CsvReadableStream({
          parseNumbers: true,
          delimiter: ";",
          parseBooleans: true,
          trim: true,
        })
      )
      .on("data", async function (row) {
        // console.log('A row arrived: ', row);
        if (row[1] == embrapa_gado_de_leite_animal_datatable[1]) {
          return;
        }
        const animalObj = {
          brinco: row[0],
          animal: row[1],
          lote: row[2],
          status: row[3],
          DEL: row[4],
          DEA: row[5],
          dataNascimento: formatDate(row[6]),
          ultimoParto: formatDate(row[7]),
          ultimaInseminacao: formatDate(row[8]),
        };
        if (animalObj.dataNascimento == null) delete animalObj.dataNascimento;
        if (animalObj.ultimoParto == null) delete animalObj.ultimoParto;
        if (animalObj.ultimaInseminacao == null)
          delete animalObj.ultimaInseminacao;

        const animal = await Animal.create(animalObj);
        await animal.save();
        // let obj ={
        //   'Brinco': row[0],
        //   'Animal': row[1],
        //   'Lote': row[2],
        //   'Status': row[3],
        //   'DEL': row[4],
        //   'DEA': row[5],
        //   'Data de nascimento': formatDate(row[6]),
        //   'Último parto': row[7],
        //   'Última inseminação': formatDate(row[8]),
        // };
      })
      .on("end", async function (data) {
        // console.log('No more rows!');
        const list = await Animal.find();
        return res.send(list).status(200);
      });
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/temperature", async (req, res) => {
  try {
    //const filepath = '../DadosTemperaturaUmidade.csv'
    let inputStream = fs.createReadStream(
      "DadosTemperaturaUmidade.csv",
      "utf8"
    );

    let DadosTemperaturaUmidade = [
      "",
      "horario",
      "temp. interna",
      "Temp. externa",
    ];

    let currentDate = "";

    inputStream
      .pipe(
        new CsvReadableStream({
          parseNumbers: true,
          delimiter: ";",
          parseBooleans: true,
          trim: true,
        })
      )
      .on("data", async function (row) {
        // console.log('A row arrived: ', row);
        if (row[1] == DadosTemperaturaUmidade[1]) {
          return;
        }

        if (row[0] != "") currentDate = row[0];
        const temperatureObj = await Temperature.create({
          date: currentDate,
          horario: row[1],
          tempInterna: formatNumber(row[2]),
          tempExterna: formatNumber(row[3]),
        });

        // console.log({
        //   'date': currentDate,
        //   'horario': row[1],
        //   'tempInterna': formatNumber(row[2]),
        //   'tempExterna': formatNumber(row[3]),
        // });
        await temperatureObj.save();
      })
      .on("end", async function (data) {
        // console.log('No more rows!');
        const listTemperature = await Temperature.find();
        return res.send(listTemperature).status(200);
      });
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/alimento", async (req, res) => {
  try {
    const { name } = req.body;
    //const filepath = '../DadosTemperaturaUmidade.csv'
    let inputStream = fs.createReadStream(name, "utf8");

    inputStream
      .pipe(
        new CsvReadableStream({
          parseNumbers: true,
          delimiter: ";",
          parseBooleans: true,
          trim: true,
          skipHeader: true,
        })
      )
      .on("data", async function (row) {
        // console.log('A row arrived: ', row);

        const alimentoObj = await Alimento.create({
          lote: row[0],
          date: row[1],
          numAnimais: formatNumber(row[2]),
          totalLote: formatNumber(row[3]),
          mediaVaca: formatNumber(row[4]),
          alimento: row[5],
        });

        console.log({
          lote: row[0],
          date: row[1],
          numAnimais: formatNumber(row[2]),
          totalLote: formatNumber(row[3]),
          mediaVaca: formatNumber(row[4]),
          alimento: row[5],
        });
        await alimentoObj.save();
      })
      .on("end", async function (data) {
        // console.log('No more rows!');
        const list = await Alimento.find();
        return res.send(list).status(200);
      });
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/prodleite", async (req, res) => {
  try {
    let inputStream = fs.createReadStream("csv/" + req.body.name, "utf8");

    let controle_leiteiro = [
      "brinco",
      "ordenha1",
      "ordenha2",
      "ordenha3",
      "prodTotal",
      "date",
    ];
    let listLeite = [];
    inputStream
      .pipe(
        new CsvReadableStream({
          parseNumbers: true,
          delimiter: ";",
          parseBooleans: true,
          trim: true,
          skipHeader: true,
        })
      )
      .on("data", async function (row) {
        // console.log('A row arrived: ', row);
        const prodLeiteObj = {
          brinco: row[0],
          ordenha1: formatNumber(row[1]),
          ordenha2: formatNumber(row[2]),
          ordenha3: formatNumber(row[3]),
          prodTotal: formatNumber(row[4]),
          date: req.body.date,
        };

        const prodLeite = await ProdLeite.create(prodLeiteObj);
        await prodLeite.save();
        // listLeite.push(prodLeiteObj)
      })
      .on("end", async function (data) {
        // console.log('No more rows!');
        const list = await ProdLeite.find();
        return res.send(list).status(200);
      });
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/prodleiteGeral", async (req, res) => {
  try {
    let inputStream = fs.createReadStream("csv/" + req.body.name, "utf8");

    let controle_leiteiro = [
      "data",
      "animais",
      "total",
      "lote1",
      "lote2",
      "lote3",
    ];
    let listLeite = [];
    inputStream
      .pipe(
        new CsvReadableStream({
          parseNumbers: true,
          delimiter: ";",
          parseBooleans: true,
          trim: true,
          skipHeader: true,
        })
      )
      .on("data", async function (row) {
        // console.log('A row arrived: ', row);
        // const prodLeiteObj = {
        //   date: row[0],
        //   animais: formatNumber(row[1]),
        //   total: formatNumber(row[2]),
        //   lote1: formatNumber(row[3]),
        //   lote2: formatNumber(row[4]),
        //   lote3: formatNumber(row[5]),
        // }

        let obj1 = {
          date: new Date(formatDate(row[0])).toISOString().split("T")[0],
          animais: formatNumber(row[1] / 3).toFixed(0),
          producao: formatNumber(row[3]),
          lote: "1",
        };
        let obj2 = {
          date: new Date(formatDate(row[0])).toISOString().split("T")[0],
          animais: formatNumber(row[1] / 3).toFixed(0),
          producao: formatNumber(row[4]),
          lote: "2",
        };
        let obj3 = {
          date: new Date(formatDate(row[0])).toISOString().split("T")[0],
          animais: formatNumber(row[1] / 3).toFixed(0),
          producao: formatNumber(row[5]),
          lote: "3",
        };

        const prodLeite1 = await ProdLeiteGeral.create(obj1);
        await prodLeite1.save();
        const prodLeite2 = await ProdLeiteGeral.create(obj2);
        await prodLeite2.save();
        const prodLeite3 = await ProdLeiteGeral.create(obj3);
        await prodLeite3.save();
        // listLeite.push(prodLeiteObj)
      })
      .on("end", async function (data) {
        // console.log('No more rows!');
        const list = await ProdLeiteGeral.find();
        return res.send(list).status(200);
      });
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.get("/balanca/leite", async (req, res) => {
  try {
    const listBrincos = await ProdLeite.distinct("brinco");

    let data = [];
    let temp_data = [];
    await Promise.all(
      listBrincos.map(async (brinco) => {
        temp_data = await getPesoLeite(brinco, Balanca, ProdLeite);
        data = [...data, ...temp_data];
      })
    );

    const fileName = "pesoXleite.csv";
    const csvWriter = createObjectCsvWriter({
      path: "csv_peso_leite/" + fileName,
      header: [
        { id: "brinco", title: "Brinco" },
        { id: "peso", title: "Peso" },
        { id: "leite", title: "Prod. Leite" },
        { id: "date", title: "date" },
      ],
    });

    try {
      await csvWriter.writeRecords(data);
      console.log("The CSV file was written successfully");
    } catch (error) {
      console.log("The CSV file was NOT written!");
    }

    return res.status(200).send({ data: data, status: "success" });
  } catch (error) {
    return res.status(500).send({ error });
  }
});

router.get("/balanca/leite/mes", async (req, res) => {
  try {
    const listBrincos = await ProdLeite.distinct("brinco");

    let data = [];
    let temp_data = [];
    await Promise.all(
      listBrincos.map(async (brinco) => {
        temp_data = await getPesoLeite(brinco, Balanca, ProdLeite);
        data = [...data, ...temp_data];
      })
    );

    let listDate = [];
    for (const item of data) {
      if (!listDate.includes(item.date)) listDate.push(item.date);
    }

    let obj = {};

    for (const date of listDate) {
      let listAnimals = data.filter((e) => e.date == date);
      let brincos = [];
      let objTemp = {};
      for (const animal of listAnimals) {
        if (!brincos.includes(animal.brinco)) {
          let brincos = listAnimals.filter((e) => e.brinco === animal.brinco);
          let brincoLeite = brincos.reduce(function (total, it) {
            return total + it.leite;
          }, 0);

          objTemp = {
            ...objTemp,
            [animal.brinco]: {
              leite: Number((brincoLeite / brincos.length).toFixed(2)),
              peso: animal.peso,
            },
          };

          brincos.push(animal.brinco);
        }
      }

      obj = {
        ...obj,
        [date]: objTemp,
      };
    }
    let consolidated = [];

    for (const key in obj) {
      if (Object.hasOwnProperty.call(obj, key)) {
        const element = obj[key];
        for (const kk in element) {
          if (Object.hasOwnProperty.call(element, kk)) {
            const item = element[kk];
            consolidated.push({
              date: key,
              brinco: kk,
              ...item,
            });
          }
        }
      }
    }

    const fileName = "pesoXleite2021.csv";
    const csvWriter = createObjectCsvWriter({
      path: "csv_peso_leite/" + fileName,
      header: [
        { id: "brinco", title: "Brinco" },
        { id: "peso", title: "Peso" },
        { id: "leite", title: "Prod. Leite" },
        { id: "date", title: "date" },
      ],
    });

    try {
      await csvWriter.writeRecords(consolidated);
      console.log("The CSV file was written successfully");
    } catch (error) {
      console.log("The CSV file was NOT written!");
    }

    return res.status(200).send({ data: consolidated, status: "success" });
  } catch (error) {
    return res.status(500).send({ error });
  }
});

router.get("/ambiente/temperature", async (req, res) => {
  try {
    // list, fileName, title, field
    const consolidated = await getAvgValueAmbiente(
      Temperature,
      "temperature_avg_dataset.csv",
      "Temperature",
      "tempInterna"
    );
    return res.status(200).send({ data: consolidated, status: "success" });
  } catch (error) {
    return res.status(500).send({ error });
  }
});
router.get("/ambiente/humidity", async (req, res) => {
  try {
    // list, fileName, title, field
    const consolidated = await getAvgValueAmbiente(
      Humidity,
      "humidity_avg_dataset.csv",
      "humidity",
      "humidityInterna"
    );
    return res.status(200).send({ data: consolidated, status: "success" });
  } catch (error) {
    return res.status(500).send({ error });
  }
});

module.exports = (app) => app.use("/api/csv", router);
