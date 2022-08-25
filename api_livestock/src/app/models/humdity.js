import mongoose from "../../database";

const HumiditySchema = new mongoose.Schema(
  {
    date: {
      type: String,
      required: true,
    },
    horario: {
      type: String,
      required: false,
    },
    humidityInterna: {
      type: Number,
      required: false,
    },
    humidityExterna: {
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

const Humidity = mongoose.model("Humidity", HumiditySchema, "humidity");

module.exports = Humidity;
