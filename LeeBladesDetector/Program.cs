using LeeBladesDetector;


if (args.Length < 1)
{
    Console.WriteLine("Uso: LeeBladesDetector <direccion_ip>");
    return;
}

var ip = args[0];
using var cliente = new ClienteVisionArtificial(ip);


var timestampUltimaImpresión = 0.0;
var paquetesRecibidos = 0;
object lockObj = new();
var hz = 0.0;

cliente.PaqueteRecibido += (_, d) =>
{
    lock (lockObj)
    {
        paquetesRecibidos++;
        var tiempoTranscurrido = d.Timestamp - timestampUltimaImpresión;
        if (tiempoTranscurrido >= 1.0)
        {
            hz = paquetesRecibidos / tiempoTranscurrido;
            timestampUltimaImpresión = d.Timestamp;
            paquetesRecibidos = 0;
        }

        Console.WriteLine(
            $"[{d.Timestamp,12:F4}] " +
            $"Yaw={d.Yaw,8:F4}  Pitch={d.Pitch,8:F4}  " +
            $"Roll=({d.Roll0:F4}, {d.Roll1:F4}, {d.Roll2:F4})  " +
            $"Eje4=({d.Cuarto0:F4}, {d.Cuarto1:F4}, {d.Cuarto2:F4}) " +
            $"Hz={hz,6:F2}"
        );
    }
};

cliente.Start();

Console.WriteLine("Pulsa ENTER para detener...\n");
Console.ReadLine();

cliente.Stop();