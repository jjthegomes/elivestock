import express from "express";
import OnFarm from "../models/onfarm";

const router = express.Router();

router.get("/", async (req, res) => {
  try {
    const list = await OnFarm.find();
    return res.send(list).status(200);
  } catch (error) {
    return res.send("erro").status(500);
  }
});

router.post("/", async (req, res) => {
  const { onfarms } = req.body;
  try {
    await Promise.all(
      onfarms.map(async (current) => {
        let item = JSON.parse(current);

        let onfarm = await OnFarm.create(item);
        await onfarm.save();
        return;
      })
    );

    return res.status(200).send({ onfarms });
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

router.get("/brinco/:brinco", async (req, res) => {
  const { brinco } = req.params;
  try {
    const list = await OnFarm.find({ brinco });

    return res.status(200).send({ list });
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

router.get("/mastite/grau", async (req, res) => {
  try {
    const listGraus = await OnFarm.distinct("grau");
    const list = await OnFarm.find().sort({ data: -1 });

    let consolidated = [];

    listGraus.forEach((grau) => {
      let opt = list.filter((e) => e.grau == grau);
      consolidated.push({
        grau: grau === "*" ? "N/A" : grau,
        total: opt.length,
      });
    });

    return res.status(200).send(consolidated);
  } catch (error) {
    res.status(400).send({ error: "erro!" });
  }
});

module.exports = (app) => app.use("/api/onfarm", router);
