import attitudes from './575047622-attitudes.json'
import {createUI} from 'attitude/ui-src'

div = document.createElement("div")
document.body.append(div)

planes = [attitudes...]
for plane in planes
  plane.color = "rgba(100,100,100,.001)"

createUI(div, planes)
