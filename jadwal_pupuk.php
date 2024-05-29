<?php

// Mendapatkan input tanggal penanaman dari user
$tanggalPenanaman = $_POST['tanggalPenanaman']; // Format: YYYY-MM-DD

// Konversi tanggal penanaman ke format DateTime
$tanggalPenanamanObj = new DateTime($tanggalPenanaman);

// Inisialisasi array untuk menyimpan data jadwal pemupukan
$jadwalPemupukan = array();

// Menentukan interval pemupukan (7 hari)
$intervalPemupukan = new DateInterval('P7D');

// Menambahkan tanggal penanaman ke array jadwal pemupukan
$jadwalPemupukan[] = $tanggalPenanamanObj;

// Melakukan loop selama 1 tahun (365 hari)
for ($i = 1; $i <= 365; $i++) {
  // Menambahkan tanggal pemupukan berikutnya ke array
  $jadwalPemupukan[] = $tanggalPenanamanObj->add($intervalPemupukan);
}

?>

<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jadwal Pemupukan</title>
</head>
<body>
  <h1>Jadwal Pemupukan</h1>

  <p>Tanggal penanaman: <?php echo $tanggalPenanaman; ?></p>

  <table>
    <tr>
      <th>Tanggal</th>
      <th>Pupuk</th>
    </tr>
    <?php foreach ($jadwalPemupukan as $tanggal): ?>
      <tr>
        <td><?php echo $tanggal->format('Y-m-d'); ?></td>
        <td>5 sendok NPK + 1 sendok Powersoil / 18 Liter Air</td>
      </tr>
    <?php endforeach; ?>
  </table>
</body>
</html>
