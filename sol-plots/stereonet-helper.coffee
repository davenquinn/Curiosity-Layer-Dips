{readFileSync} = require 'fs'
{Stereonet} = require 'attitude'
Promise = require 'bluebird'
d3 = require 'd3'
require 'd3-selection-multi'
require 'd3-jetpack'
{AzimuthLabels, DipLabels} = require 'figure-util/graticule-labels'
require './main.styl'
{subfigureLabels} = require 'figure-util'
{db, sql} = require 'syrtis-database'
chroma = require 'chroma-js'
require 'stereonet/style.styl'

setStyle = (d,i)->
  e = d3.select @
  e.classed d.instrument, true
  e.classed d.name, true

  cfunc = (max)->
    a = max/d.max_angular_error
    a = 0.8 if a > 0.8
    return a

  color = chroma(d.color)
  fill = color.alpha(cfunc(1)).css()
  stroke = color.alpha(cfunc(2)).css()

  v = e.selectAll 'path.error'
    .attrs {fill, stroke}
  console.log d,@

module.exports = (el,cb)->

  svg = d3.select(el).append 'svg.stereonet'
    .attr 'fill', 'white'

  colors = {fanUpper: '#316dbc', fanLower: '#31bc56'}

  await db.none sql('fan-deposits'), colors
  data = await db.query "SELECT * FROM mapping.__fan_deposits"

  margin = 5
  size = {height: 300, width: 300}
  innerSize = {
    height: size.height-margin-10
    width: size.width-margin-35
  }

  stereonet = Stereonet()
    .size 700
    .margin 20
    .graticule 30, 2
    .clipAngle 20
    .rectangular(innerSize)

  svg.call stereonet

  p = stereonet.projection()
    .translate([100, 100])

  stereonet.ellipses data
    .each setStyle
  stereonet.draw()

  #labels = [
    #{pos: [120,85], fill: colors.fanLower, highPriority: true, text: "Lower strata"}
    #{pos: [98,83], fill: colors.fanLower, text: "+ basin surface"}
    #{pos: [8,85], fill: colors.fanUpper, highPriority: true, text: "Upper strata"}
    #{pos: [-2,83.5], fill: colors.fanUpper, text: "+ fan surface"}
  #]

  #p = stereonet.projection()
  #e = svg
    #.append 'g.data-labels'
  #sel = e.appendMany 'text.data-label', labels
    #.text (d)->d.text
    #.attr 'fill', (d)->d.fill
    #.classed 'big', (d)->d.highPriority
    #.translate (d)->
      #console.log p(d.pos)
      #p(d.pos)

  # Graticule labels
  z = innerSize.height+margin+15
  az = new AzimuthLabels(stereonet)
    .alongLine [0,z], [innerSize.width,z]
    .textOffset [0, 15]

  az.render svg

  az.container
    .append 'text'
    .attr 'transform', "translate(#{innerSize.width/2+5} #{z+30})"
    .attr 'text-anchor', 'middle'
    .text az.labelText

  x = innerSize.width+20
  az = new AzimuthLabels(stereonet)
    .alongLine [x,5], [x,z]
    .textOffset [0, 15]

  az.render svg
    .select 'text'
    .attr 'transform', 'translate(15,0) rotate(-90)'

  az.container
    .append 'text'
    .attr 'transform', "translate(#{x+30} #{innerSize.height/2+5}) rotate(-90)"
    .attr 'text-anchor', 'middle'
    .text az.labelText

  x = innerSize.width+20
  az = new DipLabels(stereonet)
    .alongLine [100, 100], [40,innerSize.height+20]
    .textOffset [0, 15]

  az.render svg
    .select 'text'
    .attr 'transform', 'rotate(18) translate(0,5)'
    .each (d,i)->
      if i == 5
        d3.select(@).remove()

  az.container
    .append 'text'
    .attr 'transform', "translate(100,100) rotate(108) translate(120,12) rotate(-180)"
    .attr 'text-anchor', 'middle'
    .text az.labelText



  setTimeout cb, 3000


