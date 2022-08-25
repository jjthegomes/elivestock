import express from "express";
import Animal from "../models/animal";
import Balanca from "../models/balanca";
import OnFarm from "../models/onfarm";
import ProdLeite from "../models/prodleite";

const router = express.Router();

router.post("/", async (req, res) => {
  const { animais } = req.body;

  try {
    await Promise.all(
      animais.map(async (item) => {
        let animalCurrent = JSON.parse(item);

        if (animalCurrent.dataNascimento === "nan")
          delete animalCurrent.dataNascimento;

        if (animalCurrent.ultimoParto === "nan")
          delete animalCurrent.ultimoParto;

        let animal = await Animal.create(animalCurrent);
        await animal.save();
        return;
      })
    );

    return res.status(200).send({ animais });
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

router.get("/", async (req, res) => {
  try {
    const list = await Animal.find();
    return res.send(list).status(200);
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.get("/brinco/:brinco", async (req, res) => {
  const { brinco } = req.params;
  try {
    const animal = await Animal.findOne({ brinco });

    return res.status(200).send({ animal });
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});
router.get("/detalhes/:brinco", async (req, res) => {
  const { brinco } = req.params;
  try {
    const animal = await Animal.findOne({ brinco });

    const peso = await Balanca.find({ brinco });

    let onFarm = await OnFarm.find({ brinco });
    if (!onFarm.length) {
      onFarm = await OnFarm.find({ brinco: `${brinco}-1` });
    }

    onFarm.sort((a, b) => new Date(a.data) - new Date(b.data));

    const prodLeite = await ProdLeite.find({ brinco });

    return res.status(200).send({
      animal,
      onFarm,
      peso: peso.filter((e) => e.date !== "2021-8-01"),
      prodLeite: prodLeite.filter((e) => e.date !== "2021-8-01"),
    });
  } catch (error) {
    console.log(error);
    res.status(400).send({ error });
  }
});

module.exports = (app) => app.use("/api/animal", router);
