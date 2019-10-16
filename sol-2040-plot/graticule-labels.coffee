d3 = require 'd3'
import {ShapeInfo, Intersection} from 'kld-intersections'

index = {lon: 0, lat: 1}

formatAzimuthLabel = (d)->
  v = 180-d.value
  if v == 180
    return "S"
  if v == 90
    return "E"
  if v == 0
    return "N"
  if v == 270
    return "W"
  "#{v}°"

class GraticuleLabels
  type: 'lat'
  showCircles: false
  _offs: [0,0]
  _rot: 0
  labelText: 'Latitude'
  constructor: (@stereonet)->
  format: (d)->"#{d.value}°"
  alongLine: (startPos, endPos)->
    @shape = ShapeInfo.line( startPos..., endPos...)
    return @

  alongGeoPath: (obj)->
    pth = d3.geoPath(@stereonet.projection())
    d = pth(obj)
    console.log d
    @shape = ShapeInfo.path(d)
    return @

  textOffset: (offs)->
    return @_offs unless offs?
    @_offs = offs
    return @

  textRotation: (rot)->
    return @_rot unless rot?
    @_rot = rot
    return @

  getIntersections: ->
    {coordinates, type} = @stereonet.graticule()()
    pth = d3.geoPath(@stereonet.projection())
    ix = index[@type]
    intersections = []
    values = coordinates.filter (d)-> d[0][ix] == d[1][ix]
    for coords in values
      obj = {type: 'LineString', coordinates: coords}
      d = pth(obj)
      continue unless d?
      path = ShapeInfo.path(d)
      {points} = Intersection.intersect(path, @shape)
      continue unless points?
      for point in points
        point.value = coords[0][ix]
        console.log point
        intersections.push point
    return intersections

  render: (el)->
    @container = el.append 'g.labels'
    console.log @container
    v = @getIntersections()
    console.log v
    sel = @container.appendMany 'g.label', v
      .translate ({x,y})-> [x, y]
      .attrs {
        'text-anchor': 'middle'
        'alignment-baseline': 'middle'
      }

    sel.append 'text'
      .text @format
      .attr 'transform', "translate(#{@_offs[0]},#{@_offs[1]}) rotate(#{@_rot})"

    if @showCircles
      sel.append 'circle'
        .attr 'r', 2

    return sel

  renderLabel: (pos=[0,0])->
    @container.append 'text.axis-label'
      .attr 'transform', "translate(#{pos[0]}, #{pos[1]}) rotate(#{@_rot})"
      .attr 'text-anchor', 'middle'
      .text @labelText


class AzimuthLabels extends GraticuleLabels
  type: 'lon'
  labelText: 'Dip azimuth'
  format: formatAzimuthLabel

class DipLabels extends GraticuleLabels
  type: 'lat'
  labelText: 'Dip'
  format: (d)->
    v = 90-d.value
    "#{v}°"

export {GraticuleLabels, AzimuthLabels, DipLabels}


