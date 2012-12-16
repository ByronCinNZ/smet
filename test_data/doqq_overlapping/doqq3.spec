object1.description:  Image chain: /data/ear1/doqq/nc_raw/newport_ne_nc/newport_ne_nc.tif
object1.enabled:  1
object1.id:  67
object1.input_list_fixed:  1
object1.number_inputs:  0
object1.number_outputs:  1
object1.object1.apply_color_palette_flag:  1
object1.object1.description:  
object1.object1.enabled:  1
object1.object1.filename:  /data/ear1/doqq/nc_raw/newport_ne_nc/newport_ne_nc.tif
object1.object1.id:  59
object1.object1.input_list_fixed:  1
object1.object1.number_inputs:  0
object1.object1.number_outputs:  1
object1.object1.output_connection1:  72
object1.object1.output_list_fixed:  0
object1.object1.type:  ossimTiffTileSource
object1.object2.band1:  1
object1.object2.band2:  2
object1.object2.band3:  3
object1.object2.description:  
object1.object2.enabled:  0
object1.object2.id:  72
object1.object2.input_connection1:  59
object1.object2.input_list_fixed:  1
object1.object2.number_inputs:  1
object1.object2.number_output_bands:  3
object1.object2.number_outputs:  1
object1.object2.output_connection1:  71
object1.object2.output_list_fixed:  0
object1.object2.type:  ossimBandSelector
object1.object3.description:  
object1.object3.enabled:  0
object1.object3.id:  71
object1.object3.input_connection1:  72
object1.object3.input_list_fixed:  1
object1.object3.number_bands:  0
object1.object3.number_inputs:  1
object1.object3.number_outputs:  1
object1.object3.output_connection1:  70
object1.object3.output_list_fixed:  0
object1.object3.stretch_mode:  linear_one_piece
object1.object3.type:  ossimHistogramRemapper
object1.object4.description:  
object1.object4.enable_cache:  1
object1.object4.enabled:  1
object1.object4.id:  70
object1.object4.input_connection1:  71
object1.object4.input_list_fixed:  1
object1.object4.number_inputs:  1
object1.object4.number_outputs:  1
object1.object4.output_connection1:  69
object1.object4.output_list_fixed:  0
object1.object4.type:  ossimCacheTileSource
object1.object5.description:  
object1.object5.enabled:  1
object1.object5.id:  69
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
object1.object5.input_connection1:  70
object1.object5.input_list_fixed:  1
object1.object5.number_inputs:  1
object1.object5.number_outputs:  1
object1.object5.output_connection1:  68
object1.object5.output_list_fixed:  0
object1.object5.resampler.magnify_type:  nearest neighbor
object1.object5.resampler.minify_type:  nearest neighbor
object1.object5.resampler.scale_x:  0.799999999998374
object1.object5.resampler.scale_y:  0.800000000000000
object1.object5.type:  ossimImageRenderer
object1.object6.description:  
object1.object6.enable_cache:  1
object1.object6.enabled:  1
object1.object6.id:  68
object1.object6.input_connection1:  69
object1.object6.input_list_fixed:  1
object1.object6.number_inputs:  1
object1.object6.number_outputs:  1
object1.object6.output_connection1:  383
object1.object6.output_list_fixed:  0
object1.object6.type:  ossimCacheTileSource
object1.object7.cut_type:  null_outside
object1.object7.description:  
object1.object7.enabled:  1
object1.object7.geo_polygon0.datum:  NAR-C
object1.object7.geo_polygon0.number_vertices:  4
object1.object7.geo_polygon0.type:  ossimGeoPolygon
object1.object7.geo_polygon0.v0:  34.877640793649178 -76.816995529453010 -39.086744537217704
object1.object7.geo_polygon0.v1:  34.878671766627527 -76.746669318707276 -39.139506613053527
object1.object7.geo_polygon0.v2:  34.810079230918404 -76.745220322888301 -39.136539816892409
object1.object7.geo_polygon0.v3:  34.809050871215611 -76.815488269299991 -39.092349574642412
object1.object7.id:  383
object1.object7.input_connection1:  68
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
object2.filename:  /data/ear1/output/histogram_match_input/doqq3.tif
object2.id:  361
object2.image_type:  tiff_tiled_band_separate
object2.input_connection1:  67
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
