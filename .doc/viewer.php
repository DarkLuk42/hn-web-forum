<?php

	require  "../vendor/autoload.php";
	
	$parsedown = new Parsedown();
	
	$files = scandir( dirname( __FILE__ ) );
	$files = array_filter($files, function( $file ){
		return strtoupper( pathinfo( $file, PATHINFO_EXTENSION ) ) == "MD";
	});
	
	$file = $_GET["file"];
	$file = in_array( $file, $files ) ? $file : reset( $files );
	
	$html = $parsedown->text( file_get_contents( dirname( __FILE__ ) . "/" . $file ) );
	
?><!DOCTYPE html>
<html style="height: 100%;">
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1">

		<title>Markdown-Viewer</title>

		<link type="text/css" rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" />
	</head>
	<body style="height: 100%;">
		<div style="display: inline-block; height: 100%; border-right: 1px solid black; padding-right: 15px; margin-right: 15px; width: auto; vertical-align: top; overflow: hidden; overflow-y: auto;">
			<h4>Dokumentation</h4>
			<ul style="list-style: none; padding-left: 10px;">
				<?php foreach( $files AS $file ): ?>
					<li><a href="?file=<?php echo $file; ?>"><?php echo $file; ?></a></li>
				<?php endforeach; ?>
			</ul>
		</div>
		<div style="display: inline-block; height: 100%; width: auto; vertical-align: top; overflow: hidden; overflow-y: auto;"><?php echo $html; ?></div>
	</body>
</html>