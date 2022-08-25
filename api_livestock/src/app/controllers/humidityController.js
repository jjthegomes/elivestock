import express from "express";
import Humidity from "../models/humdity";

const router = express.Router();

router.post("/", async (req, res) => {
  const { humidades } = req.body;

  if (!Array.isArray(humidades))
    res.status(400).send({ error: "Objeto deve ser um array!" });

  try {
    await Promise.all(
      humidades.map(async (item) => {
        let humidity = await Humidity.create(item);
        await humidity.save();
        return;
      })
    );

    return res.status(200).send({ humidades });
  } catch (error) {
    console.log(error);
    res.status(400).send({ error: "erro!" });
  }
});

router.get("/", async (req, res) => {
  try {
    const humidades = await Humidity.find();
    return res.status(200).send(humidades);
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

module.exports = (app) => app.use("/api/humidity", router);
