import cv2 as cv

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

def validate_profile_photo(path, age, gender):
    photo = cv.imread(path)

    # Path to the required models
    faceProto = "./models/opencv_face_detector.pbtxt"
    faceModel = "./models/opencv_face_detector_uint8.pb"

    ageProto = "./models/age_deploy.prototxt"
    ageModel = "./models/age_net.caffemodel"

    genderProto = "./models/gender_deploy.prototxt"
    genderModel = "./models/gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    # ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
   
    # The age list ranges handles the rule, that have a +/- 25% variation from the original ages.
    ageList = ['(0-3)', '(3-8)', '(6-15)', '(12-25)', '(20-40)', '(30-54)', '(38-67)', '(45-125)']
    genderList = ['Male', 'Female']

    # Load the models
    ageNet = cv.dnn.readNet(ageModel, ageProto)
    genderNet = cv.dnn.readNet(genderModel, genderProto)
    faceNet = cv.dnn.readNet(faceModel, faceProto)

    # Set preferable backend and target (same as before)

    frameOpencvDnn, bboxes = getFaceBox(faceNet, photo)
    print(len(bboxes))

    # Validation for multiple faces, non-humman faces
    if len(bboxes) != 1:
        print("No face detected or multiple faces detected.")
        return False  # Not exactly one face detected

    # Get gender
    bbox = bboxes[0]
    face = frameOpencvDnn[max(0, bbox[1]):min(bbox[3], frameOpencvDnn.shape[0]), max(0, bbox[0]):min(bbox[2], frameOpencvDnn.shape[1])]

    blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPreds = genderNet.forward()
    pred_gender = genderList[genderPreds[0].argmax()]

    print("Predicted Gender:", pred_gender)

    # Validation if gender doesnot matches the given gender value
    if pred_gender != gender:
        print("Gender does not match.")
        return False  # Gender does not match

    # Get age
    ageNet.setInput(blob)
    agePreds = ageNet.forward()
    pred_age_index = agePreds[0].argmax()
    pred_age = ageList[pred_age_index]

    print("Predicted Age:", pred_age)

    # Check if the specified age falls within the predicted age range
    pred_age_min, pred_age_max = map(int, pred_age[1:-1].split('-'))
    if pred_age_min <= age <= pred_age_max:
        return True
    else:
        return False

# # Example usage
# photo = cv.imread('/media/younis/Local Disk/Orginization/LES/photo-validation/images/Photo0086.jpg')
# gender = 'Male'
# age = 13  # Example age

# valid = validate_profile_photo(photo, age, gender)
# print("Is the photo valid?", valid)

