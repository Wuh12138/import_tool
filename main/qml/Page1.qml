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

    property int verticalSpacing: 20
    property int horizontalSpacing: 10
    property int inputBoxHeight: 20
    property int inputBoxWidth: 200

    Rectangle{
        id: topBar
        width: parent.width
        height: 30
        anchors.top: parent.top
        color: "lightblue"

    }

    Rectangle{
        id: inputArea
        width: inputBoxWidth+horizontalSpacing*2
        height: inputBoxHeight*5+verticalSpacing*6

        x: parent.x+horizontalSpacing*2
        y: topBar.y+topBar.height+verticalSpacing


        TextField{
            id: neo4jUrl
            placeholderText: "Neo4j Url"
            text: "bolt://localhost:7687"

            x: parent.x+horizontalSpacing
            y: parent.y+verticalSpacing

            width: inputBoxWidth
            height: inputBoxHeight

        }

        TextField{
            id: neo4jUser
            placeholderText: "Neo4j User"
            text: "neo4j"

            x: parent.x+horizontalSpacing
            y: neo4jUrl.y+inputBoxHeight+verticalSpacing

            width: inputBoxWidth
            height: inputBoxHeight
        }

        TextField{
            id: neo4jPassword
            placeholderText: "Neo4j Password"

            x: parent.x+horizontalSpacing
            y: neo4jUser.y+inputBoxHeight+verticalSpacing

            width: inputBoxWidth
            height: inputBoxHeight

        }

        TextField{
            id: neo4jDatabase
            placeholderText: "Neo4j Database"

            x: parent.x+horizontalSpacing
            y: neo4jPassword.y+inputBoxHeight+verticalSpacing

            width: inputBoxWidth
            height: inputBoxHeight

        }

        TextField{
            id: xmindFileSelect

            placeholderText: "Xmind File Path"

            x: parent.x+horizontalSpacing
            y: neo4jDatabase.y+inputBoxHeight+verticalSpacing

            width: inputBoxWidth
            height: inputBoxHeight

            Button{
                id: selectFileButton
                text: "..."
                x: xmindFileSelect.x+xmindFileSelect.width+horizontalSpacing-10
                y: xmindFileSelectButton.y

                width: 30
                height: inputBoxHeight

                onClicked: {
                    xmindFileSelectDialog.open()
                }
            }
        }

    }



    FileDialog{

        id: xmindFileSelectDialog
        title: "Select Xmind File"

        nameFilters: ["Xmind Files (*.xmind)"]
        onAccepted: {
            xmindFileSelect.text = selectedFile
        }

    }


    Button{
        id: submitButton
        text: "Submit"

        anchors.left: parent.left
        width:parent.width
        height: 30
        y: parent.x+parent.height-this.height-10

        onClicked: {
            Page1_I.submit(neo4jUrl.text, neo4jUser.text, neo4jPassword.text, neo4jDatabase.text, xmindFileSelect.text)
        }
    }





}

