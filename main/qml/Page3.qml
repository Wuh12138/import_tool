import QtQuick
import QtQuick.Controls

Rectangle{
    id: dataImportUi
    width: 800
    height: 600

    Rectangle{
        id: scheduleUi
        anchors.top: parent.top
        anchors.left: parent.left
        width: parent.width
        height: parent.height/2-buttonArea.buttonSpacing

        ListModel{
            id: scheduleModel
            objectName: "scheduleModel"

            function addSchedule(name){
                scheduleModel.append({"name":name})
                scheduleList.currentIndex = scheduleModel.count-1
            }

        }
        ListView{
            id: scheduleList
            anchors.fill: parent
            interactive: true

            model: scheduleModel
            delegate: Rectangle{
                width: parent.width
                height: 50

                Text{
                    id: scheduleName
                    text: name
                    anchors.centerIn: parent

                    font.pixelSize: 20
                }
            }
        }

    }

    Rectangle{
        id: buttonArea
        anchors.top: scheduleUi.bottom
        anchors.left: parent.left
        width:parent.width
        height:parent.height/2


        property int buttonSpacing: 10
        Button{
            id: startButton

            anchors.top: parent.top
            x: buttonArea.buttonSpacing
            width: parent.width-buttonArea.buttonSpacing*2
            height: parent.height/2
            enabled: startButtonEnable
            Text{
                id: startButtonText
                text: "Start"
                anchors.centerIn: parent

                font.pixelSize: 20
            }

            onClicked:{
                Page3_I.start()
            }
        }

        Button{
            id:pauseButton

            anchors.top: parent.top
            x: parent.width/2
            width: parent.width/2-buttonArea.buttonSpacing*2
            height: parent.height/2
            visible: false
            enabled: false
            Text{
                id: pauseButtonText
                text: "Pause"
                anchors.centerIn: parent

                font.pixelSize: 20
            }

            onClicked: {
                if(pauseButtonText.text === "Resume")
                    {
                        pauseButtonText.text = "Pause"
                        Page3_I.resume()
                    }
                else if(pauseButtonText.text === "Pause")
                    {
                        pauseButtonText.text = "Resume"
                        Page3_I.pause()
                    }


            }
        }

        Button{
            id: stopButton

            anchors.top: startButton.bottom
            x: buttonArea.buttonSpacing
            width: parent.width/2-buttonArea.buttonSpacing*2
            height: parent.height/2
            visible: false
            Text{
                id: stopButtonText
                text: "Stop"
                anchors.centerIn: parent

                font.pixelSize: 20
            }

            onClicked: {
                Page3_I.stop()
                stopButton.enabled = false
            }
        }

        Button{
            id:goBackButton
            anchors.top:pauseButton.bottom

            x: buttonArea.buttonSpacing
            width: parent.width-buttonArea.buttonSpacing*2
            height: parent.height/2
            enabled: goBackButtonEnable
            Text{
                id: goBackButtonText
                text: "Go Back"
                anchors.centerIn: parent

                font.pixelSize: 20
            }

            onClicked: {
                Page3_I.goBack()


            }
        }
    }



}