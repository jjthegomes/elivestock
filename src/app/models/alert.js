import mongoose from "../../database";

const AlertaSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: true,
    },
    desc: {
      type: String,
      required: false,
    },
    type: {
      type: String,
      enum: ["notification", "prediction"],
      default: "notification",
    },
    seen: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  { timestamps: true }
);

const Alerta = mongoose.model("Alerta", AlertaSchema, "alertas");

module.exports = Alerta;
