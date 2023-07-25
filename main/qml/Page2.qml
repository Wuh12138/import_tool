import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt.labs.platform 1.1
import QtQuick.Dialogs

Rectangle{
    property int m_width: Screen.width/4
    property int m_height: Screen.height/2

    id: root
    width: m_width
    height: m_height

    ComboBox{
        id: comboBox
        anchors.top: parent.top
        anchors.left: parent.left

        width: 100
        height: parent.height/16

        model: ["empty", "xlsx", "MySql", "MongoDB"]
    }

    Rectangle{
        id: sourceDataLog
        x: 0
        y: comboBox.height

        width: parent.width
        height: parent.height - comboBox.height // TODO: compute submit button height


        property int horizontalSpacing: 10
        property int verticalSpacing: 10
        property int labelWidth: 200
        property int labelHeight: 20



        Rectangle{
            id: xlsxFile
            anchors.fill: parent
            visible: comboBox.currentText === "xlsx"

            TextField{
                id: xlsxFilePathSelect

                x: parent.x + sourceDataLog.horizontalSpacing
                y: parent.y + sourceDataLog.verticalSpacing

                width: parent.width - sourceDataLog.horizontalSpacing*6
                height: sourceDataLog.labelHeight
                placeholderText: "Select xlsx file"



            }


            Button{
                id: openFileSelect
                x: xlsxFilePathSelect.x + xlsxFilePathSelect.width + sourceDataLog.horizontalSpacing
                y: xlsxFilePathSelect.y

                width: xlsxFilePathSelect.height
                height: xlsxFilePathSelect.height

                text: "..."

                onClicked:{
                    xlsxFileSelectDialog.open()

                }

            }

            FileDialog{

                id: xlsxFileSelectDialog
                title: "Select Xlsx File"

                nameFilters: ["Xlsx Files (*.xlsx)"]
                property string selectedFile_: ""
                onAccepted: {
                    selectedFile_ = CIN.FormatFilePath(selectedFile)
                    xlsxFilePathSelect.text = selectedFile_
                }

            }

        }

        Rectangle{
            id: mySql
            anchors.fill: parent
            visible: comboBox.currentText === "MySql"

            TextField{
                id: mySqlHost
                x: parent.x + sourceDataLog.horizontalSpacing
                y: parent.y + sourceDataLog.verticalSpacing

                width: parent.width - sourceDataLog.horizontalSpacing*6
                height: sourceDataLog.labelHeight
                placeholderText: "Host"
            }

            TextField{
                id: mySqlPort
                x: mySqlHost.x
                y: mySqlHost.y + mySqlHost.height + sourceDataLog.verticalSpacing

                width: mySqlHost.width
                height: mySqlHost.height
                placeholderText: "Port"
            }

            TextField{
                id: mySqlUser
                x: mySqlPort.x
                y: mySqlPort.y + mySqlPort.height + sourceDataLog.verticalSpacing

                width: mySqlPort.width
                height: mySqlPort.height
                placeholderText: "User"
            }

            TextField{
                id: mySqlPassword
                x: mySqlUser.x
                y: mySqlUser.y + mySqlUser.height + sourceDataLog.verticalSpacing

                width: mySqlUser.width
                height: mySqlUser.height
                placeholderText: "Password"
            }

            TextField{
                id: mySqlDatabase
                x: mySqlPassword.x
                y: mySqlPassword.y + mySqlPassword.height + sourceDataLog.verticalSpacing

                width: mySqlPassword.width
                height: mySqlPassword.height
                placeholderText: "Database"
            }



        }


    }

    Rectangle{
        id:submitSourceDataLog

        anchors.bottom: parent.bottom
        anchors.left: parent.left

        width: parent.width
        height: parent.height/10


        Button{
            id: submitSourceDataButton
            anchors.fill: parent

            enabled: comboBox.currentText !== "empty"

            Rectangle{
                id: decoration

                anchors.fill: parent
                color: "#B5F3AF"

                visible: submitSourceDataButton.enabled

                MouseArea{
                    anchors.fill: parent

                    hoverEnabled: true

                    onEntered:{
                        decoration.color = "#4EF0AA"
                    }

                    onExited:{
                        decoration.color = "#B5F3AF"
                    }

                    property string submitSourceDataArgs: ""
                    onClicked:{
                        if (comboBox.currentText === "xlsx"){
                            submitSourceDataArgs = "xlsx " + xlsxFilePathSelect.text
                        }
                        else if (comboBox.currentText === "MySql"){
                            submitSourceDataArgs = "MySql " + mySqlHost.text + " " + mySqlPort.text + " " + mySqlUser.text + " " + mySqlPassword.text + " " + mySqlDatabase.text
                        }
                        else if (comboBox.currentText === "MongoDB"){
                            submitSourceDataArgs = "MongoDB"
                        }

                        Page2_I.submit(submitSourceDataArgs)
                    }
                }
            }

            Text{
                id: submitSourceDataText
                anchors.fill: parent
                text: "Submit"
                font.pixelSize: parent.height/3
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

        }

    }







}