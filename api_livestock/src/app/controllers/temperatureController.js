import axios from "axios";
import express from "express";
import Temperature from "../models/temperature";

const router = express.Router();

router.post("/", async (req, res) => {
  const { temperaturas } = req.body;

  if (!Array.isArray(temperaturas))
    res.status(400).send({ error: "Objeto deve ser um array!" });

  try {
    await Promise.all(
      temperaturas.map(async (item) => {
        let temperatura = await Temperature.create(item);
        await temperatura.save();
        return;
      })
    );

    return res.status(200).send({ temperaturas });
  } catch (error) {
    console.log(error);
    res.status(400).send({ error });
  }
});

router.get("/", async (req, res) => {
  try {
    const temperaturas = await Temperature.find();
    return res.status(200).send(temperaturas);
  } catch (error) {
    res.status(400).send({ error });
  }
});

module.exports = (app) => app.use("/api/temperature", router);
