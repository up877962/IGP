from yolov4.tf import YOLOv4

yolo = YOLOv4()
# yolo = YOLOv4(tiny=True)

yolo.classes = "coco.names"
yolo.input_size = (640, 480)

yolo.make_model()
yolo.load_weights("yolov4.weights", weights_type="yolo")
# yolo.load_weights("yolov4-tiny.weights", weights_type="yolo")

yolo.inference(media_path="SAMPLE.mp4", is_image=False)