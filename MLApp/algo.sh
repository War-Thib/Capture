#!/bin/sh
tensorflowjs_converter \
    --input_format='MLApp/ML_algo/my_model' \
    --output_node_names='MobilenetV1/Predictions/Reshape_1' \
    --saved_model_tags=serve \
    /mobilenet/saved_model \
    /mobilenet/web_model