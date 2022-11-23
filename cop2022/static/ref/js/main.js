//let constraints = { video: { facingMode: "user"}, audio: false};	// facingMode -> user:전면 카메라
let constraints = {
  video: { facingMode: { exact: "environment" } },
  audio: false,
}; // facingMode -> enviroment:후면 카메라
const cameraView = document.querySelector("#camera--view");
const cameraOutput = document.querySelector("#camera--output");
const cameraSensor = document.querySelector("#camera--sensor");
const cameraTrigger = document.querySelector("#camera--trigger");
const cameraUpload = document.querySelector("#camera--upload");

function cameraStart() {
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      track = stream.getTracks()[0];
      cameraView.srcObject = stream;
    })
    .catch(function (error) {
      console.error("카메라에 문제가 있습니다.", error);
    });
}

//촬영 버튼 클릭 리스너
cameraTrigger.addEventListener("click", function () {
  cameraSensor.width = cameraView.videoWidth; //640으로 정해져서 나오네?
  cameraSensor.height = cameraView.videoHeight;
  cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
  cameraOutput.src = cameraSensor.toDataURL("image/webp");
  cameraOutput.src = cameraSensor.toDataURL();
  cameraOutput.classList.add("taken");
  console.log(cameraSensor.height);

  // cameraUpload.click();
});

//현재 일자 및 시간
function getToday() {
  var date = new Date();
  var year = date.getFullYear();
  var month = ("0" + (1 + date.getMonth())).slice(-2);
  var day = ("0" + date.getDate()).slice(-2);

  var hours = ("0" + date.getHours()).slice(-2);
  var minutes = ("0" + date.getMinutes()).slice(-2);
  var seconds = ("0" + date.getSeconds()).slice(-2);
  var timeString = hours + minutes + seconds;

  return year + month + day + "_" + timeString;
}

//이미지 업로드
cameraUpload.addEventListener("click", function () {
  var imgDataUrl = cameraOutput.src;

  console.log('실행');
  //alert ("url:" + imgDataUrl);
  //var imgDataUrl = $canvas.toDataURL('image/png');

  var blobBin = atob(imgDataUrl.split(",")[1]); // base64 데이터 디코딩

  var array = [];
  for (var i = 0; i < blobBin.length; i++) {
    array.push(blobBin.charCodeAt(i));
  }

  var today = getToday();
  console.log("today:" + today);
  var fileName = "image_" + today + ".jpg";

  var file = new File([new Uint8Array(array)], fileName, {
    type: "image/jpeg",
  });

  var formdata = new FormData();
  formdata.append("file", file);

  $.ajax({
    type: "POST",
    url: "https://cop-wsvkk.run.goorm.io/upload/image",
    data: formdata,
    processData: false,
    contentType: false,
    success: function (data) {
      alert(
        "==Result==\n" +
          data.status +
          "\n" +
          "File Name:" +
          data.filename +
          "\n"
      );
    },
  });
});

// 페이지가 로드되면 함수 실행
window.addEventListener("load", cameraStart, false);

