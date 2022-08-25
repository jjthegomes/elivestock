import mongoose from "../../database";

const BalancaSchema = new mongoose.Schema(
  {
    brinco: {
      type: String,
      require: true,
    },
    peso: {
      type: Number,
      require: false,
    },
    date: {
      type: String,
      require: false,
    },
  },
  { timestamps: true }
);

const Balanca = mongoose.model("Balanca", BalancaSchema, "balanca");

module.exports = Balanca;
