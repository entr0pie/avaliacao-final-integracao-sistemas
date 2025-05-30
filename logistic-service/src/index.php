<?php

require __DIR__ . '/../vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

header('Content-Type: application/json');
$request_uri = $_SERVER['REQUEST_URI'];
$request_method = $_SERVER["REQUEST_METHOD"];

if ($request_uri == "/equipments" && $request_method == "GET") {
    $equipmentList = [
        [
            'id' => 1,
            'name' => 'Drilling Rig',
            'description' => 'Heavy-duty rig used for drilling oil wells.',
            'price' => 5000000.00
        ],
        [
            'id' => 2,
            'name' => 'Blowout Preventer',
            'description' => 'Safety device designed to seal the well in case of pressure surges.',
            'price' => 1200000.00
        ],
        [
            'id' => 3,
            'name' => 'Oil Pump',
            'description' => 'Pump system used to extract crude oil from underground reservoirs.',
            'price' => 750000.00
        ]
    ];

    echo json_encode($equipmentList);
    return;
}

if ($request_uri == "/dispatch" && $request_method == "POST") {
    $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
    $channel = $connection->channel();

    $channel->queue_declare('dispatch-messages', false, false, false, false);

    $msg = new AMQPMessage('Mensagem logistica urgentissima!!!');
    $channel->basic_publish($msg, '', 'dispatch-messages');

    $channel->close();
    $connection->close();

    $response = json_encode(["status" => "success", "message" => "Mensagem logistica urgentissima enviada"]);
    echo $response;

    return;
}

echo "Not Found!";