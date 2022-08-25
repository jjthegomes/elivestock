import { formatISO } from "date-fns";

export const formatNumber = (str) => {
  try {
    if (isNaN(Number(str))) {
      if (str.indexOf(",") != -1) {
        return Number(str.replace(",", "."));
      } else {
        console.log("caso especial", str);
        return 0;
      }
    } else {
      return str;
    }
  } catch (error) {
    console.log(error);
    return 0;
  }
};
export const formatDate = (date, separator = "/") => {
  if (date == "") return null;
  let newDate = date.split(separator);
  return new Date(newDate[2], newDate[1] - 1, newDate[0]);
};
