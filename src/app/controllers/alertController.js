import express from "express";
import Alerta from "../models/alert";

const router = express.Router();

router.get("/", async (req, res) => {
  try {
    const list = await Alerta.find().sort({ updatedAt: -1 });
    return res.send(list).status(200);
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/", async (req, res) => {
  try {
    const { alertas } = req.body;
    if (Array.isArray(alertas)) {
      await Promise.all(
        alertas.map(async (current) => {
          const alerta = await Alerta.create(current);
          await alerta.save();
          return;
        })
      );
    } else {
      const alertas = req.body;
      const alerta = await Alerta.create(alertas);
      await alerta.save();
      return res.status(200).send(alertas);
    }

    return res.status(200).send(req.body);
  } catch (error) {
    return res.status(400).send({ error });
  }
});

router.put("/:id", async (req, res) => {
  try {
    const { id } = req.params;

    const alerta = await Alerta.findById(id);
    if (alerta) {
      await Alerta.findByIdAndUpdate(id, { $set: { seen: true } });
    } else {
      return res.status(400).send({ error: "Alerta não existe" });
    }

    const list = await Alerta.find().sort({ createdAt: -1 });
    return res.send(list).status(200);
  } catch (error) {
    return res.status(400).send({ error });
  }
});
router.delete("/:id", async (req, res) => {
  try {
    const { id } = req.params;

    const alerta = await Alerta.findById(id);
    if (alerta) {
      await Alerta.deleteOne({ _id: id });
    } else {
      return res.status(400).send({ error: "Alerta não existe" });
    }

    return res.status(200).send(alerta);
  } catch (error) {
    return res.status(400).send({ error });
  }
});

module.exports = (app) => app.use("/api/alert", router);
