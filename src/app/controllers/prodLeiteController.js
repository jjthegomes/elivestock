import express from "express";
import ProdLeite from "../models/prodleite";
import ProdLeiteGeral from "../models/prodleiteGeral";
import Balanca from "../models/balanca";
import Animal from "../models/animal";
import { getPesoLeite } from "../../helpers/utils";
import { parse } from "date-fns";
import { createObjectCsvWriter } from "csv-writer";
import { formatDate } from "../../helpers/parser";

const router = express.Router();

router.get("/", async (req, res) => {
  try {
    const list = await ProdLeite.find();
    return res.send(list).status(200);
  } catch (error) {
    return res.send("erro").status(500);
  }
});
router.get("/geral", async (req, res) => {
  try {
    const list = await ProdLeiteGeral.find();
    return res.send(list).status(200);
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/", async (req, res) => {
  const { ordenhas } = req.body;

  try {
    await Promise.all(
      ordenhas.map(async (current) => {
        let item = JSON.parse(current);

        let prodleite = await ProdLeite.create(item);
        await prodleite.save();
        return;
      })
    );

    return res.status(200).send({ ordenhas });
  } catch (error) {
    console.log(error);
    res.status(400).send({ error: "erro!" });
  }
});

router.get("/brinco/:brinco", async (req, res) => {
  const { brinco } = req.params;
  try {
    const prodleite = await ProdLeite.find({ brinco }).sort({ date: 1 });

    prodleite
      .sort(function (a, b) {
        const parseA = parse(a.date, "dd-MM-yyyy", new Date());
        const parseB = parse(b.date, "dd-MM-yyyy", new Date());
        return parseB - parseA;
      })
      .reverse();
    let ordenhas = prodleite.map((e) => ({
      brinco: e.brinco,
      ordenha: Number(e.prodTotal.toFixed(2)),
      date: e.date,
    }));
    return res.status(200).send(ordenhas);
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

router.get("/consolidated", async (req, res) => {
  try {
    let prodLeite = await ProdLeite.aggregate([
      {
        $group: {
          _id: "$brinco",
          total: { $sum: "$prodTotal" },
        },
      },
    ]);

    prodLeite.sort((a, b) => b.total - a.total);

    let consolidated = [];

    await Promise.all(
      prodLeite.map(async (leite) => {
        const animal = await Animal.find({ brinco: leite._id });
        if (animal.length) {
          consolidated.push({
            ...leite,
            lote: animal[animal.length - 1].lote,
          });
        }
      })
    );

    return res.status(200).send(consolidated);
  } catch (error) {
    console.log(error);
    res.status(400).send({ error: "erro consolidated!" });
  }
});

router.get("/consolidated/date", async (req, res) => {
  try {
    const prodLeite = await ProdLeite.aggregate([
      {
        $group: {
          _id: "$date",
          total: { $sum: "$prodTotal" },
        },
      },
    ]);

    prodLeite
      .sort(function (a, b) {
        const parseA = parse(a._id, "dd-MM-yyyy", new Date());
        const parseB = parse(b._id, "dd-MM-yyyy", new Date());
        return parseB - parseA;
      })
      .reverse();

    return res.status(200).send(prodLeite);
  } catch (error) {
    console.log(error);
    res.status(400).send({ error: "erro consolidated!" });
  }
});

router.get("/consolidated/mes", async (req, res) => {
  try {
    const listBrincos = await ProdLeite.distinct("brinco");

    let data = [];
    await Promise.all(
      listBrincos.map(async (brinco) => {
        const values = await getPesoLeite(brinco, Balanca, ProdLeite);
        data = [...data, ...values];
      })
    );

    const aggregate = data.reduce((acc, curr) => {
      const date = curr.date;
      if (!acc[date]) {
        acc[date] = {
          // peso: 0,
          leite: 0,
        };
      }
      // acc[date].peso += curr.peso;
      acc[date].leite += curr.leite;
      return acc;
    }, {});

    let consolidated = [];
    for (const key in aggregate) {
      if (Object.hasOwnProperty.call(aggregate, key)) {
        const element = aggregate[key];
        consolidated.push({
          date: Number(key),
          leite: Number(element.leite.toFixed(2)),
        });
      }
    }

    return res.status(200).send(consolidated);
  } catch (error) {
    console.log(error);
    return res.status(500).send({ error });
  }
});

router.get("/consolidated/:brinco", async (req, res) => {
  const { brinco } = req.params;
  try {
    let prodLeite = await ProdLeite.aggregate([
      {
        $group: {
          _id: "$brinco",
          total: { $sum: "$prodTotal" },
        },
      },
    ]);
    return res.status(200).send(prodLeite.filter((e) => e._id == brinco));
  } catch (error) {
    console.log(error);
    res.status(400).send({ error: "erro consolidated!" });
  }
});

router.post("/consolidated/listaBrinco/", async (req, res) => {
  const { brincos } = req.body;
  try {
    let prodLeite = await ProdLeite.aggregate([
      {
        $group: {
          _id: "$brinco",
          total: { $sum: "$prodTotal" },
        },
      },
    ]);

    return res.status(200).send(prodLeite);
    // return res.status(200).send(prodLeite.filter(e => brincos.includes(e._id)));
  } catch (error) {
    console.log(error);
    res.status(400).send({ error: "erro consolidated!" });
  }
});

router.post("/consolidated/mes/listaBrinco/", async (req, res) => {
  const { brincos } = req.body;
  if (!brincos || !brincos.length)
    return res.status(400).send({ error: "LISTA DE BRINCO NAO ENVIADA" });

  try {
    let data = [];
    await Promise.all(
      brincos.map(async (brinco) => {
        const values = await getPesoLeite(brinco, Balanca, ProdLeite);
        data = [...data, ...values];
      })
    );

    const aggregate = data.reduce((acc, curr) => {
      const date = curr.date;
      if (!acc[date]) {
        acc[date] = {
          // peso: 0,
          leite: 0,
        };
      }
      // acc[date].peso += curr.peso;
      acc[date].leite += curr.leite;
      return acc;
    }, {});

    let consolidated = [];
    for (const key in aggregate) {
      if (Object.hasOwnProperty.call(aggregate, key)) {
        const element = aggregate[key];
        consolidated.push({
          date: Number(key),
          leite: Number(element.leite.toFixed(2)),
        });
      }
    }

    const prodLeiteBrinco = await ProdLeite.aggregate([
      {
        $group: {
          _id: "$brinco",
          total: { $sum: "$prodTotal" },
        },
      },
    ]);

    prodLeiteBrinco.sort((a, b) => b.total - a.total);

    const filtedBrincos = prodLeiteBrinco.filter((e) =>
      brincos.includes(e._id)
    );
    let brincosConsolidated = [];

    await Promise.all(
      filtedBrincos.map(async (leite) => {
        const animal = await Animal.find({ brinco: leite._id });
        if (animal.length) {
          brincosConsolidated.push({
            ...leite,
            lote: animal[animal.length - 1].lote,
            nome: animal[animal.length - 1].animal,
            status: animal[animal.length - 1].status,
            del: animal[animal.length - 1].DEL,
            dea: animal[animal.length - 1].DEA,
          });
        }
      })
    );

    return res.status(200).send({
      data: consolidated,
      brincos: brincosConsolidated,
    });

    // return res.status(200).send(prodLeite.filter(e => brincos.includes(e._id)));
  } catch (error) {
    console.log(error);
    res.status(400).send({ error: "erro consolidated!" });
  }
});

router.post("/csv/leite/geral/", async (req, res) => {
  try {
    const listLeite = await ProdLeiteGeral.find();
    let consolidated = [];

    for (const item of listLeite) {
      const date = new Date(item.date).toISOString().split("T")[0];
      consolidated.push({
        ...item._doc,
        date,
      });
    }

    const fileName = "leiteXlote.csv";
    const csvWriter = createObjectCsvWriter({
      path: "csv/" + fileName,
      header: [
        { id: "date", title: "Date" },
        { id: "producao", title: "Leite" },
        { id: "lote", title: "Lote" },
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
    console.log(error);
    return res.status(500).send({ error });
  }
});

module.exports = (app) => app.use("/api/prodleite", router);
