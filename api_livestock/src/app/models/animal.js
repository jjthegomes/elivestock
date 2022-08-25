import mongoose from "../../database";

const AnimalSchema = new mongoose.Schema(
  {
    brinco: {
      type: String,
      require: true,
    },
    animal: {
      type: String,
      require: false,
    },
    lote: {
      type: String,
      require: true,
    },
    status: {
      type: String,
      require: true,
    },
    DEL: {
      type: Number,
      require: false,
    },
    DEA: {
      type: Number,
      require: false,
    },
    dataNascimento: {
      type: Date,
      require: true,
    },
    ultimoParto: {
      type: Date,
      require: false,
    },
    ultimaInseminacao: {
      type: Date,
      require: false,
    },
  },
  { timestamps: true }
);

const Animal = mongoose.model("Animal", AnimalSchema, "animal");

module.exports = Animal;
