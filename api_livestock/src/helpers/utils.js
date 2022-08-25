import { formatDate } from "./parser";
import { createObjectCsvWriter } from "csv-writer";

export const getPesoFromDate = (pesos, date) => {
  let filtedPeso = pesos.filter((e) => e.date.split("-")[1] === date);
  return filtedPeso.length ? filtedPeso[0].peso : 0;
};

export const getProdLeiteTotal = (leite) => {
  return Number(
    (
      Number(leite.ordenha1) +
      Number(leite.ordenha2) +
      Number(leite.ordenha3)
    ).toFixed(2)
  );
};

export const getPesoLeite = async (brinco, Balanca, ProdLeite) => {
  const listPeso = await Balanca.find({ brinco });
  const listLeite = await ProdLeite.find({ brinco });

  let currentDate = listLeite[0].date.split("-")[1];
  let data = [];

  for (const leite of listLeite) {
    if (leite.date.split("-")[1] !== currentDate) {
      currentDate = leite.date.split("-")[1];
    }
    let currentPeso = getPesoFromDate(listPeso, currentDate);
    let total = leite.prodTotal;
    if (!leite.prodTotal) {
      total = getProdLeiteTotal(leite);
    }
    if (currentPeso) {
      data.push({
        brinco: brinco,
        leite: Number(total.toFixed(2)),
        peso: currentPeso,
        date: currentDate,
      });
    }
  }
  return data;
};

export const getAvgValueAmbiente = async (Ambiente, fileName, title, field) => {
  try {
    const ambiente = await Ambiente.find();
    let consolidated = [];
    let days = [];
    for (const item of ambiente) {
      const listTemperature = ambiente.filter((e) => e.date === item.date);
      if (!days.includes(item.date)) {
        const average = (arr) =>
          arr.reduce((prev, next) => prev + next[field], 0) / arr.length;
        consolidated.push({
          date: new Date(formatDate(item.date, "/"))
            .toISOString()
            .split("T")[0],
          average: Number(average(listTemperature).toFixed(2)),
        });
        days.push(item.date);
      }
    }

    const csvWriter = createObjectCsvWriter({
      path: "csv/" + fileName,
      header: [
        { id: "date", title: "Date" },
        { id: "average", title: title },
      ],
    });

    try {
      await csvWriter.writeRecords(consolidated);
      console.log("The CSV file was written successfully");
    } catch (error) {
      console.log("The CSV file was NOT written!");
    }

    return consolidated;
  } catch (e) {
    console.log(e);
    return [];
  }
};
