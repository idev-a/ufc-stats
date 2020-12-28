const moment = require('moment');
import Papa from "papaparse";

import { companyId } from '@/api'

// Highcharts.setOptions({
//     global: {
//         useUTC: false
//     }
// });

// mark colors based upon level

export const levelColor = (level) => {
  let color = 'green darken-1'
  level = level ? level.toLowerCase() : 'low'
  switch (level) {
    case 'high':
      color = 'red darken-4'
      break
    case 'medium':
      color = 'red lighten-1'
      break
    case 'low':
      color = 'green darken-1'
      break
  }
  return color
}

export const getActiveData = (data) => {
  return data.map(val => {
    return [
      val[0],
      parseInt(val[1] - Math.random() * 3)
    ]
  })
}

export const validEmail = (email) => {
  const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return pattern.test(email)
}

export const get_json = (val) => {
  let res = {}
  try {
    res = JSON.parse(val.answer)
  } catch(e) {}
  return res
}

export const parse_array = (val) => {
  let res = []
  try {
    res = JSON.parse(val.answer)
  } catch(e) {}
  return res
}

export const beautifyEmail = (email) => {
  if (validEmail(email)) {
    return `<a href="mailto:${email}">${email}</a>`
  } else {
    return `${email}`
  }
}

export const beautifyDuration = (duration) => {
  return moment(duration, 'x').format('HH:mm:ss')
}
export const beautifyDateTimeFromUnix = (timestamp) => {
  return moment(timestamp, 'x').format('DD MMM YYYY, HH:mm:ss')
}

export const beautifyDateTime = (date) => {
  return moment(date).format('DD MMM YYYY, HH:mm:ss')
}

export const beautifyDate = (date) => {
  if (date) {
    return moment(date).format('MMMM DD, YYYY')
  } else {
    return ''
  }
}

export const beautifyDateZ = (date) => {
  return moment(date, 'YYYYMMDDHHmmss').format('MMM DD YYYY HH:mm:ss')
}

export const removeQuotes = (val) => {
  return val.replace(/\"/g, "")
}

export const readNewLine = (val) => {
  return val.replace(/\\n/g, '<br \\>')
}

export const getTableName = (val) => {
  const _val = val.toLowerCase().replace(' ', '_');
  var letters = /^[0-9a-zA-Z_]+$/;
  let name = ''
  for (var i = 0; i < _val.length; i++) {
    if (_val.charAt(i).match(letters)) {
      name += _val.charAt(i)
    }
  }

  return name
}

export const hexEncode = (str) =>  {
  var hex, i;

  var result = "";
  for (i=0; i < str.length; i++) {
      hex = str.charCodeAt(i).toString(16);
      result += (":"+hex).slice(-4);
  }

  return result.slice(1, result.length-2)
}

export const downloadCSV = (jsonData) => {
  const parseData = Papa.unparse(jsonData)
  var blob = new Blob([parseData], { type: 'text/csv;charset=utf-8;' });

  var link = document.createElement("a");

  var url = URL.createObjectURL(blob);
  link.setAttribute("href", url);
  link.setAttribute("download", 'filename.csv');
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}