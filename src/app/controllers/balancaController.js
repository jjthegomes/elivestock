import express from "express";
import Balanca from "../models/balanca";
import ProdLeite from "../models/prodleite";
import { getPesoLeite } from "../../helpers/utils";

const router = express.Router();

router.get("/", async (req, res) => {
  try {
    const list = await Balanca.find();
    return res.send(list).status(200);
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/", async (req, res) => {
  const { pesos } = req.body;

  try {
    await Promise.all(
      pesos.map(async (current) => {
        let item = JSON.parse(current);

        if (!isNaN(item.peso)) {
          let peso = await Balanca.create(item);
          await peso.save();
        }
        return;
      })
    );

    return res.status(200).send({ pesos });
  } catch (error) {
    res.status(400).send({ error: "erro!" });
    console.log(error);
  }
});

router.get("/brinco/:brinco", async (req, res) => {
  const { brinco } = req.params;
  try {
    const balanca = await Balanca.find({ brinco });

    return res.status(200).send(balanca);
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

router.post("/date/", async (req, res) => {
  const { date } = req.body;
  try {
    const balanca = await Balanca.find({ date });

    return res.status(200).send({ balanca });
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

router.get("/leite", async (req, res) => {
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

    return res.status(200).send({ listBrincos, data });
  } catch (error) {
    console.log(error);
    return res.status(500).send({ error });
  }
});

module.exports = (app) => app.use("/api/balanca", router);
