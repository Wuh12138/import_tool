import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt.labs.platform 1.1
import QtQuick.Dialogs


Rectangle{
    id: errorDialog
    width: 400
    height: 200

    Text{
        id: errorText
        text: error_message
        anchors.centerIn: parent
    }

}
