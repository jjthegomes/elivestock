import express from "express";
import axios from "axios";

const router = express.Router();

const sendThingsBoard = async (req, ACCESS_TOKEN = "JlWxaEkocw9c25qk2Q8U") => {
  try {
    await axios({
      method: "post",
      url: `http://192.168.0.121:8080/api/v1/${ACCESS_TOKEN}/telemetry`,
      data: {
        temperature: req.body.temperature,
        humidity: req.body.humidity,
      },
    });
  } catch (error) {
    console.log(error);
  }
};

router.post("/telemetry", async (req, res) => {
  try {
    console.log("telemetry: ", req.body);
    let ACCESS_TOKEN = "JlWxaEkocw9c25qk2Q8U";
    if (req.body.device && req.body.device != "") {
      ACCESS_TOKEN = req.body.device;
    }

    await sendThingsBoard(req, ACCESS_TOKEN);

    return res.send(req.body).status(200);
  } catch (error) {
    console.log(error);
    return res.send({ res: "erro" }).status(500);
  }
});

router.post("/avg", async (req, res) => {
  try {
    // console.log('AVG: ');
    let ACCESS_TOKEN = "7UvYn9GtGOyaNHelbhUZ";
    // if (req.body.device != "") {
    //     ACCESS_TOKEN = req.body.device
    // }

    // await axios({
    //     method: 'post',
    //     url: `http://192.168.0.121:8080/api/v1/${ACCESS_TOKEN}/telemetry`,
    //     data: {
    //         temperature: req.body.temperature,
    //     }
    // });

    return res.send({ token: ACCESS_TOKEN }).status(200);
  } catch (error) {
    console.log(error);
    return res.send({ res: "erro" }).status(500);
  }
});

module.exports = (app) => app.use("/api/public", router);
