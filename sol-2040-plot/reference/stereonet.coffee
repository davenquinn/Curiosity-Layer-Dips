d3 = require 'd3'
require 'd3-selection-multi'
{chroma} = require 'chroma-js'
{Stereonet, opacityByCertainty, globalLabels} = require "attitude"
{AzimuthLabels, DipLabels} = require 'figure-util/graticule-labels'

scale = d3.scaleLinear().domain([2,10]).range([0.8,0.2]).clamp(true)

c = (d)->d.color
opacityScale = opacityByCertainty(c, 'path.error')
  .alphaScale scale

classify = (sel)->
   sel
    .classed 'in-group', (d)->d.inGroup
    .classed 'is-group', (d)->d.members?

createVerticalStereonet = (el_, data, size)->
  innerSize = {
    width: size.width-50
    height: size.height-25
  }

  stereonet = Stereonet()
    .size 400
    .margin 5
    .graticule 10, 1
    .clipAngle 3
    .center [0,-90]
    .rectangular(innerSize)

  el = d3.select el_
    .append 'g'
    .call stereonet

  stereonet.projection()
    .translate [0,100]

  stereonet
    .ellipses data
    .call classify
    .each (d)->
      d3.select @
        .attrs {stroke: d.color, fill: d.color}
    .on 'mouseover', (d)->console.log d.uid

  stereonet.draw()

  # Graticule labels
  z = innerSize.height+5
  az = new DipLabels(stereonet)
    .alongLine [0,z], [innerSize.width,z]
    .textOffset [0, 15]

  az.render el

  az.container
    .append 'text'
    .attr 'transform', "translate(5 #{z+15})"
    .attr 'text-anchor', 'start'
    .text az.labelText

  x = innerSize.width+5
  az = new AzimuthLabels(stereonet)
    .alongLine [x,5], [x,z]
    .textOffset [10,0]

  az.render el
    .select 'text'
    .attr 'transform', 'translate(15,0) rotate(-90)'

  az.container
    .append 'text'
    .attr 'transform', "translate(#{x+30} #{innerSize.height/2+5}) rotate(-90)"
    .attr 'text-anchor', 'middle'
    .text az.labelText

module.exports = {createVerticalStereonet, opacityScale}




