import mongoose from "../../database";

const IntelligenceSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },
    fileName: {
      type: String,
      required: false,
    },
    desc: {
      type: String,
      required: false,
    },
    active: {
      type: Boolean,
      required: true,
      default: false,
    },
    type: {
      type: String,
      enum: ["peso", "alimento", "animais", "ontology"],
      default: "peso",
    },
    mse: {
      type: Number,
      required: true,
    },
    rmse: {
      type: Number,
      required: true,
    },
    mae: {
      type: Number,
      required: true,
    },
    r2: {
      type: Number,
      required: true,
    },
  },
  { timestamps: true }
);

const Intelligence = mongoose.model(
  "Intelligence",
  IntelligenceSchema,
  "intelligence"
);

module.exports = Intelligence;
