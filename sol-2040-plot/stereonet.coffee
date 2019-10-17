import h from 'react-hyperscript'
# Need some sort of CSS or else we get an error in bundler
import Promise from 'bluebird'
import chroma from 'chroma-js'
import * as d3 from 'd3'
require 'd3-selection-multi'
import 'd3-jetpack'
import {Stereonet} from '../deps/Attitude/js-frontend/lib/attitude.js'
import {nest} from 'd3-collection'
import {Component} from 'react'
import {findDOMNode} from 'react-dom'
import './main.styl'
import {AzimuthLabels, DipLabels} from './graticule-labels'

class StereonetComponent extends Component
  @defaultProps: {
    filterData: false
    clipAngle: 20
    margin: 20
    width: 300,
    height: 300,
    graticule: [30, 5]
  }
  render: ->
    {width, height, margin} = @props
    width = width+2*margin
    height = height+2*margin
    h 'svg.stereonet', {width, height}

  componentDidMount: ->
    {data, stackedData,
     clipAngle, graticule, margin, width, height} = @props

    el = findDOMNode(@)
    innerSize = {
      height
      width
    }

    sz = Math.max(width, height)

    stereonet = Stereonet()
      .size sz
      .margin @props.margin
      .graticule(graticule...)
      .clipAngle clipAngle
      .rectangular(innerSize)

    stereonet.rotate([157+180,-76, 90])
    stereonet.scale(sz*4)

    svg = d3.select(el)
      .append 'g'
    svg.call stereonet

    stereonet
      .projection()
      .translate([innerSize.width/2+margin,innerSize.height/2+margin])

    svg.select '.neatline'
      .attr 'fill', 'transparent'
      .attr 'stroke-width', '2px'

    svg.select '.graticule'
      .attr 'fill', 'transparent'
      .attr 'stroke-width', '1px'
      .attr 'stroke', '#aaa'
      .attr 'stroke-dasharray', '2,2'

    ell2 = null
    if stackedData?
      ell2 = stereonet.ellipses stackedData
    ell = stereonet.ellipses data

    stereonet.draw()

    console.log ell

    ell.each (d)->
      console.log d.color
      el = d3.select(@).select('.error')
      #if d.min_angular_error < 10
      c = chroma(d.color)
      fill = c.alpha(0.1).css()
      #else
      el.attr 'fill', fill
      el.attr 'stroke', c.css()

    return unless ell2?

    ell2.each (d)->
      el = d3.select(@).select('.error')
      fill = 'transparent'
      #if d.min_angular_error < 10
      opacity = 1/d.min_angular_error/d.min_angular_error
      if opacity > 0.2
        opacity = 0.2
      if opacity < 0.05
        opacity = 0.05
      fill = "rgba(0,0,0,0.8)"
      #else
      #  el.attr 'stroke-dasharray', '4,2'
      el.attr 'stroke', fill
      el.style 'stroke-width', '3px'
      el.attr 'stroke-dasharray', '8,4'
      el.attr 'fill', "rgba(0,0,0,0.1)"

    console.log "Rendering azimuth labels"
    azLabels = new AzimuthLabels stereonet

    azContainer = svg.append("g.azimuth-labels")

    azLabels
      .alongLine([width+margin,margin], [width+margin, height+margin])
      .render azContainer
      .selectAll('text')
      .attr 'transform', 'rotate(90) translate(0 -3)'
      .attr 'alignment-baseline', 'center'

    azLabels = new AzimuthLabels stereonet
    azLabels
      .alongLine([margin,margin], [width+margin, margin])
      .render azContainer
      .selectAll('text')
      .attr 'transform', 'translate(0 -3)'
      .attr 'alignment-baseline', 'center'


    console.log "Rendering dip labels"
    dipLabels = new DipLabels stereonet

    v = stereonet.projection().rotate()
    coords = {type: "LineString", coordinates: [[-15,90], [-15,90-24]]}

    dipLabels
      #.alongLine([margin,height+margin], [width+margin, height+margin])
      .alongGeoPath(coords)
      .render svg.append("g.dip-labels")
      .selectAll('text')
      .attr "transform", "rotate(-52)"
      .attr 'alignment-baseline', 'middle'

export default StereonetComponent

