object1.description:  Image chain: /data/ear1/doqq/nc_raw/newport_nw_nc/newport_nw_nc.tif
object1.enabled:  1
object1.id:  94
object1.input_list_fixed:  1
object1.number_inputs:  0
object1.number_outputs:  1
object1.object1.apply_color_palette_flag:  1
object1.object1.description:  
object1.object1.enabled:  1
object1.object1.filename:  /data/ear1/doqq/nc_raw/newport_nw_nc/newport_nw_nc.tif
object1.object1.id:  86
object1.object1.input_list_fixed:  1
object1.object1.number_inputs:  0
object1.object1.number_outputs:  1
object1.object1.output_connection1:  99
object1.object1.output_list_fixed:  0
object1.object1.type:  ossimTiffTileSource
object1.object2.band1:  1
object1.object2.band2:  2
object1.object2.band3:  3
object1.object2.description:  
object1.object2.enabled:  0
object1.object2.id:  99
object1.object2.input_connection1:  86
object1.object2.input_list_fixed:  1
object1.object2.number_inputs:  1
object1.object2.number_output_bands:  3
object1.object2.number_outputs:  1
object1.object2.output_connection1:  98
object1.object2.output_list_fixed:  0
object1.object2.type:  ossimBandSelector
object1.object3.description:  
object1.object3.enabled:  0
object1.object3.id:  98
object1.object3.input_connection1:  99
object1.object3.input_list_fixed:  1
object1.object3.number_bands:  0
object1.object3.number_inputs:  1
object1.object3.number_outputs:  1
object1.object3.output_connection1:  97
object1.object3.output_list_fixed:  0
object1.object3.stretch_mode:  linear_one_piece
object1.object3.type:  ossimHistogramRemapper
object1.object4.description:  
object1.object4.enable_cache:  1
object1.object4.enabled:  1
object1.object4.id:  97
object1.object4.input_connection1:  98
object1.object4.input_list_fixed:  1
object1.object4.number_inputs:  1
object1.object4.number_outputs:  1
object1.object4.output_connection1:  96
object1.object4.output_list_fixed:  0
object1.object4.type:  ossimCacheTileSource
object1.object5.description:  
object1.object5.enabled:  1
object1.object5.id:  96
object1.object5.image_view_trans.type:  ossimImageViewProjectionTransform
object1.object5.image_view_trans.view_proj.central_meridian:  -75.000000000000000
object1.object5.image_view_trans.view_proj.datum:  NAR-C
object1.object5.image_view_trans.view_proj.ellipse_code:  RF
object1.object5.image_view_trans.view_proj.ellipse_name:  GRS 80
object1.object5.image_view_trans.view_proj.hemisphere:  N
object1.object5.image_view_trans.view_proj.major_axis:  6378137.000000000000000
object1.object5.image_view_trans.view_proj.meters_per_pixel_x:  10.000000000000000
object1.object5.image_view_trans.view_proj.meters_per_pixel_y:  10.000000000000000
object1.object5.image_view_trans.view_proj.minor_axis:  6356752.314100000075996
object1.object5.image_view_trans.view_proj.origin_latitude:  0.000000000000000
object1.object5.image_view_trans.view_proj.tie_point_easting:  500000.000000000000000
object1.object5.image_view_trans.view_proj.tie_point_northing:  0.000000000000000
object1.object5.image_view_trans.view_proj.type:  ossimUtmProjection
object1.object5.image_view_trans.view_proj.zone:  18
object1.object5.input_connection1:  97
object1.object5.input_list_fixed:  1
object1.object5.number_inputs:  1
object1.object5.number_outputs:  1
object1.object5.output_connection1:  95
object1.object5.output_list_fixed:  0
object1.object5.resampler.magnify_type:  nearest neighbor
object1.object5.resampler.minify_type:  nearest neighbor
object1.object5.resampler.scale_x:  0.799999999998411
object1.object5.resampler.scale_y:  0.799999999998817
object1.object5.type:  ossimImageRenderer
object1.object6.description:  
object1.object6.enable_cache:  1
object1.object6.enabled:  1
object1.object6.id:  95
object1.object6.input_connection1:  96
object1.object6.input_list_fixed:  1
object1.object6.number_inputs:  1
object1.object6.number_outputs:  1
object1.object6.output_connection1:  280
object1.object6.output_list_fixed:  0
object1.object6.type:  ossimCacheTileSource
object1.object7.cut_type:  null_outside
object1.object7.description:  
object1.object7.enabled:  1
object1.object7.geo_polygon0.datum:  NAR-C
object1.object7.geo_polygon0.number_vertices:  4
object1.object7.geo_polygon0.type:  ossimGeoPolygon
object1.object7.geo_polygon0.v0:  34.877590772842680 -76.879573792352943 -39.040149154465190
object1.object7.geo_polygon0.v1:  34.878659569467985 -76.809140676640340 -39.092539351658061
object1.object7.geo_polygon0.v2:  34.810069360219181 -76.807639873415880 -39.097177668213973
object1.object7.geo_polygon0.v3:  34.809003272650941 -76.878014642331166 -39.053477546173148
object1.object7.id:  280
object1.object7.input_connection1:  95
object1.object7.input_list_fixed:  1
object1.object7.number_inputs:  1
object1.object7.number_outputs:  0
object1.object7.number_polygons:  1
object1.object7.output_list_fixed:  0
object1.object7.type:  ossimGeoPolyCutter
object1.output_connection1:  -1
object1.output_list_fixed:  0
object1.type:  ossimImageChain
object2.color_lut_flag:  0
object2.compression_quality:  75
object2.compression_type:  none
object2.create_envi_hdr:  0
object2.create_external_geometry:  0
object2.create_fgdc:  0
object2.create_histogram:  1
object2.create_image:  1
object2.create_jpeg_world_file:  0
object2.create_overview:  1
object2.create_readme:  0
object2.create_tiff_world_file:  0
object2.description:  
object2.enabled:  1
object2.filename:  /data/ear1/output/histogram_match_input/doqq2.tif
object2.id:  258
object2.image_type:  tiff_tiled_band_separate
object2.input_connection1:  94
object2.input_list_fixed:  1
object2.number_inputs:  1
object2.number_outputs:  0
object2.output_geotiff_flag:  1
object2.output_list_fixed:  0
object2.output_tile_size_x:  64
object2.output_tile_size_y:  64
object2.overview_compression_quality:  75
object2.overview_compression_type:  1
object2.pixel_type:  point
object2.projection.units:  meters
object2.type:  ossimTiffWriter
product.pixel_type:  PIXEL_IS_POINT
product.projection.central_meridian:  -75.000000000000000
product.projection.datum:  NAR-C
product.projection.ellipse_code:  RF
product.projection.ellipse_name:  GRS 80
product.projection.hemisphere:  N
product.projection.major_axis:  6378137.000000000000000
product.projection.meters_per_pixel_x:  10.000000000000000
product.projection.meters_per_pixel_y:  10.000000000000000
product.projection.minor_axis:  6356752.314100000075996
product.projection.origin_latitude:  0.000000000000000
product.projection.tie_point_easting:  500000.000000000000000
product.projection.tie_point_northing:  0.000000000000000
product.projection.type:  ossimUtmProjection
product.projection.zone:  18
