require 'require-yaml'
# Script for headless generation of orientation figures
d3 = require 'd3'
require 'd3-selection-multi'
require 'd3-jetpack'
{db, sql} = require 'syrtis-database'
setupMapData = require './setup'
setupStereonet = require '../../orientations/map/stereonet'
{StaticMap} = require 'gis-core'
{getMeasurements} = require '../../orientations/map/data'
regroupData = require '../../orientations/map/regroup-data'
{createVerticalStereonet} = require './stereonet'
require './main.styl'
{exec} = require 'child-process-promise'
escape = require 'shell-escape'
{subfigureLabelsUnordered} = require 'figure-util'

dpi = 96
mapsz =
  width: 4*dpi
  height: 3*dpi

sz =
  width: 8*dpi
  height: 6*dpi

l = mapsz.width

{readFileSync} = require 'fs'
{getFigureExtent} = require 'figure-util'

module.exports =  (el_,cb)->

  elementsForComparison = [2476, 2477]
  groupedElements = [2478, 2462,2475,2471,2470]

  loc = await getFigureExtent id: 'grouped-plane-example'
  map = new StaticMap mapsz, loc, "ortho"

  data = await getMeasurements loc.id, map.extent
  data = data.filter (d)->
      [
        elementsForComparison...,
        groupedElements...
      ].includes d.id

  fn = regroupData([groupedElements])
  data = await fn(data)

  for d in data
    d.isComparison = elementsForComparison.includes d.id
    d.inGroup = groupedElements.includes d.id
    if d.isComparison
      d.color = '#aaaaaa'
    else
      d.color = 'red'

  el = d3.select el_
    .append 'div#container'
    .styles {width: sz.width}

  map_el = el.append 'svg.map'
  ste_el = el.append 'svg.stereonet'
    .attrs mapsz

  scale = {ndivs: 4}

  await map.create(map_el, {scale})
  setupMapData(map, data)
  createVerticalStereonet(ste_el.node(),data, mapsz)

  el.selectAll 'svg'
    .each subfigureLabelsUnordered('text', 'ADBC')

  cmd = escape ['python', require.resolve('./cartesian.py'), groupedElements...]
  console.log cmd
  {stdout} = await exec cmd, maxBuffer: 1000*1024

  el.append 'div'
    .html stdout

  cb()


