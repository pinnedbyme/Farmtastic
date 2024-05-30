<?php

// Create an array to store the schedule
$schedule = array();

// Check if the form has been submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the planting date from the form
    $plantingDate = date_create($_POST["plantingDate"]);

    // Calculate the number of days in a year
    $daysInAYear = 365;

    // Calculate the number of weeks in a year
    $weeksInAYear = ceil($daysInAYear / 7);

    // Loop through each week in a year
    for ($i = 0; $i < $weeksInAYear; $i++) {
        // Calculate the date of the current week
        $currentDate = date_create();
        date_sub($currentDate, date_interval_create_from_date_string($i * 7 . ' days'));
        date_format($currentDate, 'Y-m-d');

        // Add the schedule entry
        $schedule[] = array(
            'date' => $currentDate,
            'fertilizer' => '5 sendok NPK + 1 sendok powersoil'
        );
    }

    // Print the schedule
    ?>
    <div class="container">
        <h1>Fertilization Schedule</h1>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Fertilizer</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($schedule as $entry) { ?>
                    <tr>
                        <td><?php echo $entry['date']; ?></td>
                        <td><?php echo $entry['fertilizer']; ?></td>
                    </tr>
                <?php } ?>
            </tbody>
        </table>
    </div>
    <?php
} else {
    // Print the form
    ?>
    <div class="container">
        <h1>Fertilization Schedule</h1>
        <form method="post">
            <label for="plantingDate">Enter your planting date:</label>
            <input type="date" id="plantingDate" name="plantingDate" required>
            <button type="submit">Generate Schedule</button>
        </form>
    </div>
    <?php
}

?>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
</body>
</html>
