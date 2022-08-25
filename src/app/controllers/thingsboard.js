import express from "express";
import axios from "axios";
import { CronJob } from "cron";

const router = express.Router();

const sendThingsBoard = async (req, ACCESS_TOKEN = "gDRX70SsBM8I41X0Zr6B") => {
  try {
    await axios({
      method: "post",
      url: `http://localhost:9090/api/v1/${ACCESS_TOKEN}/telemetry`,
      data: req.body,
    });
  } catch (error) {
    console.log(error);
  }
};

router.post("/telemetry/:device", async (req, res) => {
  try {
    await sendThingsBoard(req, req.params.device);
    return res.send(req.body).status(200);
  } catch (error) {
    console.log(error);
    return res.send({ res: "erro" }).status(500);
  }
});

router.post("/interno/:device", async (req, res) => {
  try {
    let currentTemp = req.body.temperature;
    let MaxTemp = currentTemp + 10;

    console.log("Before job instantiation 1");
    const job = new CronJob("0 */1 * * * *", async function () {
      const d = new Date();
      console.log("Every one Minute:", d, currentTemp);
      await sendThingsBoard(
        { body: { temperature: currentTemp } },
        req.params.device
      );
      currentTemp++;
      if (currentTemp === MaxTemp) job.stop();
    });
    // console.log('After job instantiation 1');
    job.start();

    return res.send({ msg: "success" }).status(200);
  } catch (error) {
    console.log(error);
    return res.send({ res: "erro" }).status(500);
  }
});

router.post("/externo/:device", async (req, res) => {
  try {
    let currentTemp = req.body.temperature;
    let MaxTemp = currentTemp + 10;

    console.log("Before job instantiation 2");
    const job = new CronJob("0 */1 * * * *", async function () {
      const d = new Date();
      console.log("Every one Minute:", d, currentTemp);
      await sendThingsBoard(
        { body: { temperature: currentTemp } },
        req.params.device
      );
      currentTemp++;
      if (currentTemp === MaxTemp) job.stop();
    });
    // console.log('After job instantiation 2');
    job.start();

    return res.send({ msg: "success" }).status(200);
  } catch (error) {
    console.log(error);
    return res.send({ res: "erro" }).status(500);
  }
});

module.exports = (app) => app.use("/api/thingsboard", router);
