const moment = require('moment');
import Papa from "papaparse";

import { companyId } from '@/api'

// Highcharts.setOptions({
//     global: {
//         useUTC: false
//     }
// });

export const validEmail = (email) => {
  const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return pattern.test(email)
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
  if (date) {
    return moment(date).format('DD MMM YYYY, HH:mm:ss')
  } else {
    return ""
  }
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

export const readNewLine = (val) => {
  return val.replace(/\\n/g, '<br \\>')
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

export const downloadCSV = (jsonData, filename='filename.csv') => {
  const parseData = Papa.unparse(jsonData)
  var blob = new Blob([parseData], { type: 'text/csv;charset=utf-8;' });

  var link = document.createElement("a");

  var url = URL.createObjectURL(blob);
  link.setAttribute("href", url);
  link.setAttribute("download", filename);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

export const parseTimestamp = (timestamp, format = '') => {
  if (!timestamp) return

  const date = timestamp
    ? new Date(timestamp)
    : timestamp

  if (format === 'HH:mm') {
    return `${zeroPad(date.getHours(), 2)}:${zeroPad(date.getMinutes(), 2)}`
  } else if (format === 'DD MMMM YYYY') {
    const options = { month: 'long', year: 'numeric', day: 'numeric' }
    return `${new Intl.DateTimeFormat('en-GB', options).format(date)}`
  } else if (format === 'DD/MM/YY') {
    const options = { month: 'numeric', year: 'numeric', day: 'numeric' }
    return `${new Intl.DateTimeFormat('en-GB', options).format(date)}`
  } else if (format === 'DD MMMM, HH:mm') {
    const options = { month: 'long', day: 'numeric' }
    return `${new Intl.DateTimeFormat('en-GB', options).format(
      date
    )}, ${zeroPad(date.getHours(), 2)}:${zeroPad(date.getMinutes(), 2)}`
  }

  return date
}

const zeroPad = (num, pad) => {
  return String(num).padStart(pad, '0')
}

export const isSameDay = (d1, d2) => {
  return (
    d1.getFullYear() === d2.getFullYear() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getDate() === d2.getDate()
  )
}