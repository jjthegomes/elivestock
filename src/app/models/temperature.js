import mongoose from "../../database";

const TemperatureSchema = new mongoose.Schema(
  {
    date: {
      type: String,
      required: true,
    },
    horario: {
      type: String,
      required: false,
    },
    tempInterna: {
      type: Number,
      required: false,
    },
    tempExterna: {
      type: Number,
      required: false,
    },
    source: {
      type: String,
      required: false,
      default: "sensor",
    },
  },
  { timestamps: true }
);

const Temperature = mongoose.model(
  "Temperature",
  TemperatureSchema,
  "temperature"
);

module.exports = Temperature;
