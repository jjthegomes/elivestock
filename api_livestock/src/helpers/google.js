import { google } from "googleapis";
import path from "path";
import os from "os";
import readline from "readline";
import fs from "fs";

// If modifying these scopes, delete token.json.
export const SCOPES = [
  "https://www.googleapis.com/auth/drive.metadata.readonly",
  "https://www.googleapis.com/auth/drive",
  "https://www.googleapis.com/auth/drive.appdata",
  "https://www.googleapis.com/auth/drive.file",
  "https://www.googleapis.com/auth/drive.metadata",
  "https://www.googleapis.com/auth/drive.photos.readonly",
  "https://www.googleapis.com/auth/drive.readonly",
];
// The file token.json stores the user's access and refresh tokens, and is
// created automatically when the authorization flow completes for the first
// time.
export const TOKEN_PATH = "./src/resources/token.json";
export const currentClient = {
  web: {
    client_id:
      "51558278109-ghbtdl7acf87qojhoasighu029ch4s9b.apps.googleusercontent.com",
    project_id: "projeto-teste-72664",
    auth_uri: "https://accounts.google.com/o/oauth2/auth",
    token_uri: "https://oauth2.googleapis.com/token",
    auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs",
    client_secret: "785el0ZmPmciQMPc8qmOC6nP",
    redirect_uris: ["http://localhost:3000/oauth2callback"],
    javascript_origins: ["http://localhost:3000", "http://localhost:3001"],
  },
};

export const currentToken = {
  access_token:
    "ya29.a0AfH6SMDaN1iHg3QprvKRU2kmI3dnsp4JhC7yI7dORNIWStXgJtQjkJbvtEgnL-1UwT5tGoVcIal_fhlf2VgRD03w8ElW4mmrHd977WSi3GlE5HYKM3DL3yJld2H12AZvm3YDYNV60w_bw6SXp4gARRxlrqBu",
  scope:
    "https://www.googleapis.com/auth/drive.photos.readonly https://www.googleapis.com/auth/drive.scripts https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata",
  token_type: "Bearer",
  expires_in: 3599,
  refresh_token:
    "1//042rso_6upEefCgYIARAAGAQSNwF-L9IrSHxa_sK2u5Fu7pPI8HfARPsiDWye23Owkjqf_hvmJ3t2ksdEocvVhK2dGtCjwFMkP-4",
};

// Temperatura-Umidade: 1Y6a1PbPqnbJ8Bd65yOhRukyh2whevHF7
// Peso: 1_3zsh10hdX5TaPzp0nN10zG5f55Dn7tV
// Mastite: 1_dOpX726EdbcjoTzT5tyuIdMUg68dqas
// Controle-leiteiro: 1YA9o8P1CZIZm97Xjay2lZWDx07b8U
// Animais: 1fJ71AMGkK3vc_S8WW5CygZHJSHmd4eoy
// Alimentação: 1P3j2jLchtMFTUlk0g6uq6dpJbtLklPwv
export const FoldersID = [
  {
    id: "1aQnajI8CQ5OgAiCiYLi4XqGoCi3bYo8a",
    folderName: "03_08_21",
    type: "Temperatura-Umidade",
  },
  { id: "11nFrSJf6rzlwCCiUOcci4h1QJqGkatw7", folderName: "Peso", type: "Peso" },
  {
    id: "1_dOpX726EdbcjoTzT5tyuIdMUg68dqas",
    folderName: "Mastite",
    type: "Mastite",
  },
  {
    id: "1cv_wZG5uhSRHap9AQHQzrU27ae8gJhV5",
    folderName: "7- Jul",
    type: "Controle-leiteiro",
  }, //individual
  {
    id: "1fJ71AMGkK3vc_S8WW5CygZHJSHmd4eoy",
    folderName: "Animais",
    type: "Animais",
  },
  {
    id: "1P3j2jLchtMFTUlk0g6uq6dpJbtLklPwv",
    folderName: "Alimentação",
    type: "Alimentação",
  },
];

/**
 * Create an OAuth2 client with the given credentials, and then execute the
 * given callback function.
 * @param {Object} credentials The authorization client credentials.
 * @param {function} callback The callback to call with the authorized client.
 */
export function authorize(credentials, callback) {
  const { client_secret, client_id, redirect_uris } = credentials.web;
  const oAuth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    redirect_uris[0]
  );

  // Check if we have previously stored a token.
  fs.readFile(TOKEN_PATH, (err, token) => {
    if (err) return getAccessToken(oAuth2Client, callback);
    oAuth2Client.setCredentials(JSON.parse(token));
    callback(oAuth2Client);
  });
}

/**
 * Get and store new token after prompting for user authorization, and then
 * execute the given callback with the authorized OAuth2 client.
 * @param {google.auth.OAuth2} oAuth2Client The OAuth2 client to get token for.
 * @param {getEventsCallback} callback The callback for the authorized client.
 */
export function getAccessToken(oAuth2Client, callback) {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: "offline",
    scope: SCOPES,
  });
  console.log("Authorize this app by visiting this url:", authUrl);
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question("Enter the code from that page here: ", (code) => {
    rl.close();
    oAuth2Client.getToken(code, (err, token) => {
      if (err) return console.error("Error retrieving access token", err);
      oAuth2Client.setCredentials(token);
      // Store the token to disk for later program executions
      fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
        if (err) return console.error(err);
        console.log("Token stored to", TOKEN_PATH);
      });

      callback(oAuth2Client);
    });
  });
}

/**
 * Lists the names and IDs of up to 10 files.
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 */
export async function defaultGoogleDriveFunction(auth) {
  const drive = google.drive({ version: "v3", auth });
  drive.files.list(
    {
      q: "name contains 'Onfarm'",
      pageSize: 50,
      fields: "nextPageToken, files(id, name)",
    },
    (err, res) => {
      if (err) return console.log("The API returned an error: " + err);
      const files = res.data.files;
      if (files.length) {
        console.log("Files:");
        files.map((file) => {
          console.log(`${file.name} (${file.id})`);
        });
      } else {
        console.log("No files found.");
      }
    }
  );
}

export async function listFilesByName(auth, fileName) {
  const drive = google.drive({ version: "v3", auth });
  try {
    const response = await drive.files.list({
      q: `name contains '${fileName}'`,
      pageSize: 50,
      // fields: 'nextPageToken, files(id, name, mimeType, parents)',
      fields: "nextPageToken, files(id, name, parents)",
    });
    return response.data.files ? response.data.files : [];
  } catch (error) {
    console.log("The API returned an error: " + error);
    return [];
  }
}

export async function listFolderByName(auth, fileName) {
  const drive = google.drive({ version: "v3", auth });
  try {
    const response = await drive.files.list({
      q: `mimeType='application/vnd.google-apps.folder' and name contains '${fileName}'`,
      pageSize: 50,
      fields: "nextPageToken, files(id, name, mimeType, parents)",
    });
    return response.data.files ? response.data.files : [];
  } catch (error) {
    console.log("The API returned an error: " + error);
    return [];
  }
}

/**
 *Download file based on IDs
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 * @param {String} fileId ID
 * @param {String} fileName name of the file
 * @param {String} extension extension of the file
 */
export async function downloadFile(auth, fileId, fileName, extension) {
  const drive = google.drive({ version: "v3", auth });
  return await drive.files
    .get({ fileId, alt: "media" }, { responseType: "stream" })
    .then((res) => {
      return new Promise((resolve, reject) => {
        const filePath = `${os.homedir()}/Desktop/${fileName}`;
        console.log(`writing to ${filePath}.${extension}`);
        const dest = fs.createWriteStream(filePath + "." + extension);
        let progress = 0;

        res.data
          .on("end", () => {
            console.log("Done downloading file.");
            return resolve(filePath);
          })
          .on("error", (err) => {
            console.error("Error downloading file.");
            reject(err);
          })
          .on("data", (d) => {
            progress += d.length;
            if (process.stdout.isTTY) {
              process.stdout.clearLine();
              process.stdout.cursorTo(0);
              process.stdout.write(`Downloaded ${progress} bytes\n`);
            }
          })
          .pipe(dest);
      });
    })
    .catch((e) => {
      console.log(e);
    });
}
