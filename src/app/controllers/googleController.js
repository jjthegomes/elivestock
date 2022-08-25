import fs from "fs";
import express from "express";

import { google } from "googleapis";
import { CronJob } from "cron";
import {
  TOKEN_PATH,
  currentClient,
  currentToken,
  FoldersID,
  authorize,
  getAccessToken,
  defaultGoogleDriveFunction,
  listFilesByName,
  listFolderByName,
  downloadFile,
} from "../../helpers/google";

const router = express.Router();

router.get("/requestToken", async (req, res) => {
  // Load client secrets from a local file.
  fs.readFile("./src/resources/credentials.json", (err, content) => {
    if (err) return console.log("Error loading client secret file:", err);
    // Authorize a client with credentials, then call the Google Drive API.

    authorize(JSON.parse(content), defaultGoogleDriveFunction); //default
  });
  return res.status(200);
});

router.post("/download", async (req, res) => {
  const { fileId, fileName } = req.body;

  if (!fileId || !fileName)
    return res
      .status(500)
      .send({ status: "fail", erro: "file id and extension required" });

  try {
    const { client_secret, client_id, redirect_uris } = currentClient.web;
    const oAuth2Client = new google.auth.OAuth2(
      client_id,
      client_secret,
      redirect_uris[0]
    );

    await oAuth2Client.setCredentials(currentToken);

    let response = await downloadFile(
      oAuth2Client,
      fileId,
      fileName.split(".")[0],
      fileName.split(".")[1]
    );
    return res
      .status(200)
      .send({ status: "success", data: { file: fileName, path: response } });
  } catch (e) {
    return res.status(500).send({ status: "fail", erro: e });
  }
});

router.post("/listByName", async (req, res) => {
  if (!req.body.name)
    return res
      .status(500)
      .send({ status: "fail", erro: "file name is required" });

  try {
    // Authorize a client with credentials, then call the Google Drive API.
    const { client_secret, client_id, redirect_uris } = currentClient.web;
    const oAuth2Client = new google.auth.OAuth2(
      client_id,
      client_secret,
      redirect_uris[0]
    );

    // Check if we have previously stored a token.
    await oAuth2Client.setCredentials(currentToken);
    let files = await listFilesByName(oAuth2Client, req.body.name);

    let driveFiles = [];
    files.map((file) => {
      // console.log(`${file.name} (${file.id}) | Folder ${file.parents}`);
      for (const item of FoldersID) {
        if (file.parents[0] === item.id) {
          // file.folder = item.type
          driveFiles.push({
            id: file.id,
            folder: item.type,
            name: file.name,
          });
        }
      }
    });

    return res.status(200).send({ status: "success", data: driveFiles });
  } catch (e) {
    console.log(e);
    return res.status(500).send({ status: "fail", erro: e });
  }
});

router.post("/listByFolderName", async (req, res) => {
  if (!req.body.name)
    return res
      .status(500)
      .send({ status: "fail", đerro: "folder name is required" });

  try {
    // Authorize a client with credentials, then call the Google Drive API.
    const { client_secret, client_id, redirect_uris } = currentClient.web;
    const oAuth2Client = new google.auth.OAuth2(
      client_id,
      client_secret,
      redirect_uris[0]
    );
    // Check if we have previously stored a token.
    await oAuth2Client.setCredentials(currentToken);

    let files = await listFolderByName(oAuth2Client, req.body.name);
    return res.status(200).send({ status: "success", data: files });
  } catch (e) {
    console.log(e);
    return res.status(500).send({ status: "fail", erro: e });
  }
});

router.post("/agendar", async (req, res) => {
  try {
    console.log("Starting at ", new Date());
    const job = new CronJob(
      "0-59 * * * *",
      () => {
        console.log("tarefa executada", new Date());
      },
      null,
      true,
      "America/Sao_Paulo"
    );
    return res.status(200).send({ ok: "ok" });
  } catch (e) {
    console.log(e);
    return res.status(500).send({ erro: e });
  }
});

router.post("/agendarDia", async (req, res) => {
  try {
    //puxar todo dia 10 do mes
    const job = new CronJob(
      "0 0 10 * *",
      () => {
        console.log("---------------------");
        console.log("Running Cron Job");
      },
      null,
      true,
      "America/Sao_Paulo"
    );
    return res.status(200).send({ ok: "ok" });
  } catch (e) {
    console.log(e);
    return res.status(500).send({ erro: e });
  }
});

module.exports = (app) => app.use("/api/google", router);
