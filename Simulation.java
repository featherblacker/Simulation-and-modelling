class Simulation{



	Public static void main(String args[]){
		Inspector1Time = 5;
		Inspector2Time2 = 3;
		Inspector2Time3 = 4;
		SIGMA = 0.6;
		long seed = Long.parseLong(argv[0]);
		Sequence = new Random(seed);
	}


	public static void Initialization(){
		Clock = 0.0;
		QueueLength11 = 0;
		QueueLength12 = 0;
		QueueLength13 = 0;
		QueueLength22 = 0;
		QueueLength33 = 0;
		NumberInStation1 = 0;
		NumberInStation2 = 0;
		NumberInStation3 = 0;
		LastEventTime11 = 0;
		LastEventTime12 = 0;
		LastEventTime13 = 0;
		LastEventTime22 = 0;
		LastEventTime33 = 0;
		TotalBusy
		SumResponseTime = 0;
		NumberOfDepartures1 = 0;
		NumberOfDepartures2 = 0;
		NumberOfDepartures3 = 0;
	}

	public static void ProcessArrival(Event evt){
		
	}
}