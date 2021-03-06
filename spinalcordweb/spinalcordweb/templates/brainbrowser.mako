<%inherit file="main_template.mako"/>

<link type="text/css" href="${request.static_url('spinalcordweb:static/css/volume-viewer-demo.css')}" rel="Stylesheet" />
<link type="text/css" href="${request.static_url('spinalcordweb:static/css/common.css')}" rel="Stylesheet" />
<link type="text/css" href="${request.static_url('spinalcordweb:static/css/ui-darkness/jquery-ui-1.8.10.custom.css')}" rel="Stylesheet" />

<header id="head" class="secondary"></header>
<!-- container -->
<div class="container">

    <ol class="breadcrumb">
        <li><a href="${request.route_url('home')}">Home</a></li>
        <li class="active">3D Viewer</li>
    </ol>
    <br>
    <button class="fold_reply btn">Fold the toolbox</button>
    <div class="container">
        <div class="row">
            <div class="col-md-3 no-float toolb">
                <!-- The ToolBox-->
                <%include file="toolbox.mako"/>
                <!--/The ToolBox -->
            </div>

            <div id="bb" class="col-md-9 no-float">

                <header class="page-header">
                <h1 class="page-title">3D Viewer (Volume slicer)</h1>
                </header>

                <!--
                  BrainBrowser: Web-based Neurological Visualization Tools
                  (https://brainbrowser.cbrain.mcgill.ca)

                  Copyright (C) 2011
                  The Royal Institution for the Advancement of Learning
                  McGill University

                  This program is free software: you can redistribute it and/or modify
                  it under the terms of the GNU Affero General Public License as
                  published by the Free Software Foundation, either version 3 of the
                  License, or (at your option) any later version.

                  This program is distributed in the hope that it will be useful,
                  but WITHOUT ANY WARRANTY; without even the implied warranty of
                  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                  GNU Affero General Public License for more details.

                  You should have received a copy of the GNU Affero General Public License
                  along with this program.  If not, see <http://www.gnu.org/licenses/>.


                  Author: Tarek Sherif <tsherif@gmail.com> (http://tareksherif.ca/)
                  Author: Nicolas Kassis
                -->

                <script id="volume-ui-template" type="x-volume-ui-template">
                  <div id="volume-viewer">
                      <div class="volume-viewer-display ">
                      </div>

                      <div class="volume-viewer-controls volume-controls">

                        <div id="config-right">

                          <div class="coords">
                            <div class="control-heading" id="voxel-coordinates-heading-{{VOLID}}">
                              Voxel Coordinates:
                            </div>
                            <div class="voxel-coords" data-volume-id="{{VOLID}}">
                              I:<input id="voxel-i-{{VOLID}}" class="control-inputs">
                              J:<input id="voxel-j-{{VOLID}}" class="control-inputs">
                              K:<input id="voxel-k-{{VOLID}}" class="control-inputs">
                            </div>
                              <br>
                            <div class="control-heading" id="world-coordinates-heading-{{VOLID}}">
                              World Coordinates:
                                <br>
                            </div>
                            <div class="world-coords" data-volume-id="{{VOLID}}">
                              X:<input id="world-x-{{VOLID}}" class="control-inputs">
                              Y:<input id="world-y-{{VOLID}}" class="control-inputs">
                              Z:<input id="world-z-{{VOLID}}" class="control-inputs">
                            </div>
                              <br>
                          </div>

                          <div id="intensity-value-div-{{VOLID}}">
                            <span class="control-heading" data-volume-id="{{VOLID}}">
                              Value:
                            </span>
                            <span id="intensity-value-{{VOLID}}" class="intensity-value"></span>
                          </div>
                            <br>

                          <div id="color-map-{{VOLID}}">
                            <span class="control-heading" id="color-map-heading-{{VOLID}}">
                              Color Map:
                            </span>
                          </div>
                            <br>

                          <div id="color-map-file-{{VOLID}}" class="color-map-file-div" data-volume-id="{{VOLID}}" >
                            <span class="control-heading">Color map file: </span><input type="file" name="color-map-file-{{VOLID}}" class="color-map-file">
                          </div>
                            <br>

                        </div>
                        <div id="config-left">

                          <div class="threshold-div" data-volume-id="{{VOLID}}">
                            <div class="control-heading">
                              Threshold:
                            </div>
                            <div class="thresh-inputs">
                              <input id="min-threshold-{{VOLID}}" class="control-inputs thresh-input-left" value="0"/>
                              <input id="max-threshold-{{VOLID}}" class="control-inputs thresh-input-right" value="1300"/>
                            </div>
                            <div class="slider volume-viewer-threshold" id="threshold-slider-{{VOLID}}"></div>
                          </div>

                          <div id="time-{{VOLID}}" class="time-div" data-volume-id="{{VOLID}}" style="display:none">
                            <span class="control-heading">Time:</span>
                            <input class="control-inputs" value="0" id="time-val-{{VOLID}}"/>
                            <div class="slider volume-viewer-threshold" id="time-slider-{{VOLID}}"></div>
                            <input type="checkbox" class="button" id="play-{{VOLID}}"><label for="play-{{VOLID}}">Play</label>
                          </div>

                          <div class="contrast-div" data-volume-id="{{VOLID}}">
                            <span class="control-heading" id="contrast-heading{{VOLID}}">Contrast (0.0 to 2.0):</span>
                            <input class="control-inputs" value="1.0" id="contrast-val"/>
                            <div id="contrast-slider" class="slider volume-viewer-contrast"></div>
                          </div>

                          <div class="brightness-div" data-volume-id="{{VOLID}}">
                            <span class="control-heading" id="brightness-heading{{VOLID}}">Brightness (-1 to 1):</span>
                            <input class="control-inputs" value="0" id="brightness-val"/>
                            <div id="brightness-slider" class="slider volume-viewer-brightness"></div>
                          </div>

                          <div id="slice-series-{{VOLID}}" class="slice-series-div" data-volume-id="{{VOLID}}">
                            <div class="control-heading" id="slice-series-heading-{{VOLID}}">All slices: </div>
                            <span class="slice-series-button button" data-axis="xspace">Sagittal</span>
                            <span class="slice-series-button button" data-axis="yspace">Coronal</span>
                            <span class="slice-series-button button" data-axis="zspace">Transverse</span>
                          </div>
                        </div>
                      </div>
                  </div>
                </script>
                <!-- <div id="brainbrowser-wrapper" style="display:none">
                  <div id="volume-viewer"> -->
                    <div id="global-controls" class="volume-viewer-controls">
                      <span class="control-heading">Volume type:</span>
                      <select id="volume-type">
                        <option value="structural">Structural</option>
                        <option value="functional">Functional</option>
                        <option value="file">Load your own volume!</option>
                      </select>
                      <span class="control-heading">Panel size:</span>
                      <select id="panel-size">
                        <option value="128">128</option>
                        <option value="200">200</option>
                        <option value="233" SELECTED>233</option>
                        <option value="350">350</option>
                        <option value="512">512</option>
                      </select>
                      <span id="sync-volumes-wrapper">
                        <input type="checkbox" class="button" id="sync-volumes"><label for="sync-volumes">Synchronize</label>
                      </span>
                      <span id="screenshot" class="button">Screenshot</span>
                      <div id="volume-file" class="file-select">
                        <div>
                          <span class="control-heading">Header file: </span><input type="file" name="header-file" id="header-file">
                        </div>
                        <div>
                          <span class="control-heading">Raw data file: </span><input type="file" name="raw-data-file" id="raw-data-file">
                        </div>
                        <div id="volume-file-hint">
                          Use
                          <a href="scripts/minc2volume-viewer.js" target="_blank">minc2volume-viewer.js</a>
                          or
                          <a href="scripts/minc2volume-viewer.py" target="_blank">minc2volume-viewer.py</a>
                          to convert your MINC files into the header and raw data files required by the volume viewer (requires
                          installation of the <a href="http://www.bic.mni.mcgill.ca/ServicesSoftware/MINC" target="_blank">MINC tools</a>).
                        </div>
                        <div id="volume-file-submit">
                          <span class="button">Load raw/header</span>
                        </div>
                        <div>
                          <span class="control-heading">Nifti file: </span><input type="file" name="nii-file" id="nii-file">
                        </div>
                        <div id="volume-file-submit-nifti">
                          <span class="button">Load niti</span>
                        </div>
                      </div>
                      <div class="instructions">Shift-click to drag. Hold ctrl to measure distance.</div>
                    </div>
                    <div id="brainbrowser"></div>
                    <input type="hidden" id='nii_path' value="${file_path}">
                  </div>


                    </div>
                </div>
            </div>

        <div class="row">
        <!-- Sidebar -->
            <aside class="col-md-4 sidebar sidebar-left">


            </aside>
            <!-- /Sidebar -->

            <!-- Article main content -->
            <article class="col-md-8 maincontent">

            </article>
        </div>
    </div>	<!-- /container -->

<script src="${request.static_url('spinalcordweb:static/js/viewer/ui.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/brainbrowser.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/core/tree-store.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/lib/config.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/lib/utils.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/lib/events.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/lib/loader.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/lib/color-map.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer/lib/display.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer/lib/panel.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer/lib/utils.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer/modules/loading.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer/modules/rendering.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer/volume-loaders/overlay.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer/volume-loaders/minc.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/brainbrowser/volume-viewer/volume-loaders/nifti1.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/viewer/gunzip.min.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/volume-viewer.config.js')}"></script>
<script src="${request.static_url('spinalcordweb:static/js/volume-viewer.js')}"></script>
<script>
    $(".fold_reply").click(function() {
        $("#bb").toggleClass('col-md-9 col-md-12');
        $(".toolb").toggle(0);
        })
</script>