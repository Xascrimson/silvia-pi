var curtemp = new TimeSeries();
var settemp = new TimeSeries();
var settempm = new TimeSeries();
var settempp = new TimeSeries();
var pterm = new TimeSeries();
var iterm = new TimeSeries();
var dterm = new TimeSeries();
var pidval = new TimeSeries();
var avgpid = new TimeSeries();
var lastreqdone = 1;
var timeout;

function refreshinputs() {
	$.getJSON({
		url: "/allstats",
		timeout: 500,
		success: function (resp) {
			console.log(resp);
			$("#inputSetTemp").val(resp.settemp);
			$("#inputSnooze").val(resp.snooze);
			$("#inputSetSteamTemp").val(resp.steamtemp);
		},
	});
	$.getJSON({
		url: "/alltime",
		timeout: 500,
		success: function (resp) {
			console.log(resp);
			$("#inputTimerOnMo").val(resp.TimerOnMo);
			$("#inputTimerOffMo").val(resp.TimerOffMo);
			$("#inputTimerOnTu").val(resp.TimerOnTu);
			$("#inputTimerOffTu").val(resp.TimerOffTu);
			$("#inputTimerOnWe").val(resp.TimerOnWe);
			$("#inputTimerOffWe").val(resp.TimerOffWe);
			$("#inputTimerOnTh").val(resp.TimerOnTh);
			$("#inputTimerOffTh").val(resp.TimerOffTh);
			$("#inputTimerOnFr").val(resp.TimerOnFr);
			$("#inputTimerOffFr").val(resp.TimerOffFr);
			$("#inputTimerOnSa").val(resp.TimerOnSa);
			$("#inputTimerOffSa").val(resp.TimerOffSa);
			$("#inputTimerOnSu").val(resp.TimerOnSu);
			$("#inputTimerOffSu").val(resp.TimerOffSu);
		},
	});
}

function resettimer() {
	clearTimeout(timeout);
	timeout = setTimeout(refreshinputs, 30000);
}

function onresize() {
	var h;
	if ($(window).height() * 0.5 > 450) {
		h = 450;
	} else {
		h = $(window).height() * 0.5;
	}

	$("#chart").attr("width", $("#fullrow").width() - 30);
	$("#chart").attr("height", h);
	$("#pidchart").attr("width", $("#fullrow").width() - 30);
	$("#pidchart").attr("height", h);

	if ($(document).width() < 600) {
		$("#toggleadv").html("Adv Stats");
	} else {
		$("#toggleadv").html("Advanced Stats");
	}
}

$(document).ready(function () {
	resettimer();
	$(this).mousemove(resettimer);
	$(this).keypress(resettimer);

	onresize();
	$(window).resize(onresize);

	createTimeline();

	$(".adv").hide();
	$("#toggleadv").click(function () {
		$(".adv").toggle();
	});

	// $(".timer").hide();
	$("#btnSchedule").click(() => {
		$(".timer").toggle();
	});

	refreshinputs();

	$("#inputSetTemp").change(function () {
		$.post("/settemp", { settemp: $("#inputSetTemp").val() });
	});

	$("#inputSetSteamTemp").change(function () {
		$.post("/setsteamtemp", { steamtemp: $("#inputSetSteamTemp").val() });
	});

	$("#btnSnooze").click(function () {
		$.post("/snooze", { snooze: $("#inputSnooze").val() });
		$("#btnSnooze").hide();
		$("#btnSnoozeC").show();
	});

	$("#btnSnoozeC").click(function () {
		$.post("/resetsnooze");
		$("#btnSnooze").show();
		$("#btnSnoozeC").hide();
	});

	$("#inputTimerOnMo").change(function () {
		console.log("changing timer on", $("#inputTimerOnMo").val());
		$.post("/TimerOnMo", { TimerOnMo: $("#inputTimerOnMo").val() });
	});

	$("#inputTimerOffMo").change(function () {
		$.post("/TimerOffMo", { TimerOffMo: $("#inputTimerOffMo").val() });
	});

	$("#inputTimerOnTu").change(function () {
		$.post("/TimerOnTu", { TimerOnTu: $("#inputTimerOnTu").val() });
	});

	$("#inputTimerOffTu").change(function () {
		$.post("/TimerOffTu", { TimerOffTu: $("#inputTimerOffTu").val() });
	});

	$("#inputTimerOnWe").change(function () {
		$.post("/TimerOnWe", { TimerOnWe: $("#inputTimerOnWe").val() });
	});

	$("#inputTimerOffWe").change(function () {
		$.post("/TimerOffWe", { TimerOffWe: $("#inputTimerOffWe").val() });
	});

	$("#inputTimerOnTh").change(function () {
		$.post("/TimerOnTh", { TimerOnTh: $("#inputTimerOnTh").val() });
	});

	$("#inputTimerOffTh").change(function () {
		$.post("/TimerOffTh", { TimerOffTh: $("#inputTimerOffTh").val() });
	});

	$("#inputTimerOnFr").change(function () {
		$.post("/TimerOnFr", { TimerOnFr: $("#inputTimerOnFr").val() });
	});

	$("#inputTimerOffFr").change(function () {
		$.post("/TimerOffFr", { TimerOffFr: $("#inputTimerOffFr").val() });
	});

	$("#inputTimerOnSa").change(function () {
		$.post("/TimerOnSa", { TimerOnSa: $("#inputTimerOnSa").val() });
	});

	$("#inputTimerOffSa").change(function () {
		$.post("/TimerOffSa", { TimerOffSa: $("#inputTimerOffSa").val() });
	});

	$("#inputTimerOnSu").change(function () {
		$.post("/TimerOnSu", { TimerOnSu: $("#inputTimerOnSu").val() });
	});

	$("#inputTimerOffSu").change(function () {
		$.post("/TimerOffSu", { TimerOffSu: $("#inputTimerOffSu").val() });
	});
});

setInterval(function () {
	if (lastreqdone == 1) {
		$.getJSON({
			url: "/allstats",
			timeout: 500,
			success: function (resp) {
				if (resp.snoozeon == true) {
					$("#btnSnooze").hide();
					$("#btnSnoozeC").show();
				} else {
					$("#btnSnooze").show();
					$("#btnSnoozeC").hide();
				}

				// TODO, need to CHANGE this to also get resp.steampin to ensure we are showing the steaming phase
				curtemp.append(new Date().getTime(), resp.tempc);
				if (resp.steam) {
					settemp.append(new Date().getTime(), resp.steamtemp);
					settempm.append(new Date().getTime(), resp.steamtemp - 4);
					settempp.append(new Date().getTime(), resp.steamtemp + 4);
				} else {
					settemp.append(new Date().getTime(), resp.settemp);
					settempm.append(new Date().getTime(), resp.settemp - 4);
					settempp.append(new Date().getTime(), resp.settemp + 4);
				}
				pterm.append(new Date().getTime(), resp.pterm);
				iterm.append(new Date().getTime(), resp.iterm);
				dterm.append(new Date().getTime(), resp.dterm);
				pidval.append(new Date().getTime(), resp.pidval);
				avgpid.append(new Date().getTime(), resp.avgpid);

				$("#curtemp").html(resp.tempc.toFixed(2));
				$("#pterm").html(resp.pterm.toFixed(2));
				$("#iterm").html(resp.iterm.toFixed(2));
				$("#dterm").html(resp.dterm.toFixed(2));
				$("#pidval").html(resp.pidval.toFixed(2));
				$("#avgpid").html(resp.avgpid.toFixed(2));
			},
			complete: function () {
				lastreqdone = 1;
			},
		});

		lastreqdone = 0;
	}
}, 100);

function createTimeline() {
	var chart = new SmoothieChart({
		grid: { verticalSections: 3 },
		minValueScale: 1.05,
		maxValueScale: 1.05,
	});
	chart.addTimeSeries(settemp, { lineWidth: 1, strokeStyle: "#ffff00" });
	chart.addTimeSeries(settempm, { lineWidth: 1, strokeStyle: "#ffffff" });
	chart.addTimeSeries(settempp, { lineWidth: 1, strokeStyle: "#ffffff" });
	chart.addTimeSeries(curtemp, { lineWidth: 3, strokeStyle: "#ff0000" });
	chart.streamTo(document.getElementById("chart"), 500);

	var pidchart = new SmoothieChart({
		grid: { verticalSections: 3 },
		minValueScale: 1.05,
		maxValueScale: 1.05,
	});
	pidchart.addTimeSeries(pterm, { lineWidth: 2, strokeStyle: "#ff0000" });
	pidchart.addTimeSeries(iterm, { lineWidth: 2, strokeStyle: "#00ff00" });
	pidchart.addTimeSeries(dterm, { lineWidth: 2, strokeStyle: "#0000ff" });
	pidchart.addTimeSeries(pidval, { lineWidth: 2, strokeStyle: "#ffff00" });
	pidchart.addTimeSeries(avgpid, { lineWidth: 2, strokeStyle: "#ff00ff" });
	pidchart.streamTo(document.getElementById("pidchart"), 500);
}
