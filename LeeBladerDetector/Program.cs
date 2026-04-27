using LeeBladesDetector;


if (args.Length < 1)
{
    Console.WriteLine("Uso: LeeBladesDetector <direccion_ip>");
    return;
}

var ip = args[0];
using var cliente = new ClienteVisionArtificial(ip);

cliente.PaqueteRecibido += (_, d) =>
{
    Console.WriteLine(
        $"[{d.Timestamp,12:F4}] " +
        $"Yaw={d.Yaw,8:F4}  Pitch={d.Pitch,8:F4}  " +
        $"Roll=({d.Roll0:F4}, {d.Roll1:F4}, {d.Roll2:F4})  " +
        $"Eje4=({d.Cuarto0:F4}, {d.Cuarto1:F4}, {d.Cuarto2:F4})"
    );
};

cliente.Start();

Console.WriteLine("Pulsa ENTER para detener...\n");
Console.ReadLine();

cliente.Stop();