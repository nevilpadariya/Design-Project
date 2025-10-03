import sys
from typing import Optional

class BalloonFestival:
    def __init__(self, yourBalloonNames: list[str]) -> None:
        """Initialize the class with a list of unique balloon names"""
        self.balloon_names = set(yourBalloonNames)
        self.balloons = {}  # balloon_name -> {'altitude': float, 'flying': bool, 'stable': bool, 'unstable_since': float or None}
        self.wind_conditions = {}  # altitude -> {'speed': float, 'timestamp': float}
        self.competitors = {}  # balloon_name -> altitude (for non-team balloons)
        
    def balloon_ascended(self, timestamp: float, balloonName: str, altitude: float) -> bool:
        """Register that a balloon has ascended to a given altitude"""
        if balloonName in self.balloon_names:
            # Team balloon
            if balloonName in self.balloons:
                # Update existing balloon - repeated calls update altitude
                self.balloons[balloonName]['altitude'] = altitude
                self.balloons[balloonName]['flying'] = True
            else:
                # New balloon ascending
                self.balloons[balloonName] = {
                    'altitude': altitude,
                    'flying': True,
                    'stable': True,  # Stable by default upon ascending
                    'unstable_since': None
                }
            
            # Check stability based on current wind conditions
            self._update_balloon_stability(balloonName, timestamp)
            return True
        else:
            # Competitor balloon - always update to latest altitude
            self.competitors[balloonName] = altitude
            return True
            
    def balloon_descended(self, timestamp: float, balloonName: str) -> bool:
        """Register that a balloon has descended to the ground"""
        if balloonName not in self.balloon_names:
            return False
            
        if balloonName not in self.balloons or not self.balloons[balloonName]['flying']:
            return False
            
        # Reset balloon to default state after descending
        self.balloons[balloonName] = {
            'altitude': 0,
            'flying': False,
            'stable': True,
            'unstable_since': None
        }
        return True
        
    def set_wind_speed(self, timestamp: float, altitude: float, windSpeed: float) -> bool:
        """Update wind speed centered at a specific altitude"""
        self.wind_conditions[altitude] = {
            'speed': windSpeed,
            'timestamp': timestamp
        }
        
        # Update stability for all flying balloons
        for balloon_name in self.balloons:
            if self.balloons[balloon_name]['flying']:
                self._update_balloon_stability(balloon_name, timestamp)
                
        return True
        
    def inspect_balloons(self, timestamp: float) -> list[str]:
        """Return sorted names of stable balloons at or above highest stable competitor altitude"""
        # Update all balloon stabilities before inspection
        for balloon_name in self.balloons:
            if self.balloons[balloon_name]['flying']:
                self._update_balloon_stability(balloon_name, timestamp)
        
        # Find highest STABLE competitor altitude
        highest_stable_competitor_altitude = 0
        for competitor_name, altitude in self.competitors.items():
            # Check if this competitor would be stable at their altitude
            competitor_wind_speed = self._calculate_wind_speed_at_altitude(altitude)
            if competitor_wind_speed <= 15:  # Stable competitor
                highest_stable_competitor_altitude = max(highest_stable_competitor_altitude, altitude)
        
        # Find stable team balloons at or above the threshold
        stable_balloons = []
        for balloon_name, balloon_data in self.balloons.items():
            if (balloon_data['flying'] and 
                balloon_data['stable'] and 
                balloon_data['altitude'] >= highest_stable_competitor_altitude):
                stable_balloons.append(balloon_name)
                
        return sorted(stable_balloons)
        
    def _calculate_wind_speed_at_altitude(self, target_altitude):
        """Calculate effective wind speed at target altitude based on all wind conditions"""
        if not self.wind_conditions:
            return 0
            
        total_speed = 0
        for wind_altitude, wind_data in self.wind_conditions.items():
            wind_speed_at_altitude = wind_data['speed']
            # Apply the wind speed formula
            speed_contribution = wind_speed_at_altitude / (1 + ((target_altitude - wind_altitude) / 100) ** 2)
            total_speed += speed_contribution
            
        return total_speed
        
    def _update_balloon_stability(self, balloon_name, current_timestamp):
        """Update balloon stability based on current wind conditions"""
        if balloon_name not in self.balloons or not self.balloons[balloon_name]['flying']:
            return
            
        balloon = self.balloons[balloon_name]
        current_wind_speed = self._calculate_wind_speed_at_altitude(balloon['altitude'])
        
        if current_wind_speed > 15:  # Exceeds threshold
            if balloon['stable']:
                # Balloon becomes unstable
                balloon['stable'] = False
                balloon['unstable_since'] = current_timestamp
        else:  # Below threshold
            if not balloon['stable'] and balloon['unstable_since'] is not None:
                # Check if balloon has been in safe conditions for 300+ seconds
                if current_timestamp - balloon['unstable_since'] >= 300:
                    balloon['stable'] = True
                    balloon['unstable_since'] = None


def main() -> None:
    balloon_festival: Optional[BalloonFestival] = None
    while True:
        try:
            line: str = input()
        except EOFError:
            sys.exit(0)
            
        parameters: list[str] = line.split()
        keyword: str = parameters[0]
        args: list[str] = [i for i in parameters[1:]]
        
        if keyword == "Init":
            assert len(args) >= 1
            assert balloon_festival is None, "Init should only be called once"
            balloon_festival = BalloonFestival(args)
        elif keyword == "BalloonAscended":
            assert len(args) == 3
            assert balloon_festival is not None, "Init should be called before any other command"
            timestamp: float = float(args[0])
            balloon_name: str = args[1]
            altitude: float = float(args[2])
            ascended_result: bool = balloon_festival.balloon_ascended(timestamp, balloon_name, altitude)
            print(f"BalloonAscended={ascended_result}")
        elif keyword == "BalloonDescended":
            assert len(args) == 2
            assert balloon_festival is not None, "Init should be called before any other command"
            timestamp: float = float(args[0])
            balloon_name: str = args[1]
            descended_result: bool = balloon_festival.balloon_descended(timestamp, balloon_name)
            print(f"BalloonDescended={descended_result}")
        elif keyword == "SetWindSpeed":
            assert len(args) == 3
            assert balloon_festival is not None, "Init should be called before any other command"
            timestamp: float = float(args[0])
            altitude: float = float(args[1])
            wind_speed: float = float(args[2])
            set_wind_result: bool = balloon_festival.set_wind_speed(timestamp, altitude, wind_speed)
            print(f"SetWindSpeed={set_wind_result}")
        elif keyword == "InspectBalloons":
            assert len(args) == 1
            assert balloon_festival is not None, "Init should be called before any other command"
            timestamp: float = float(args[0])
            inspect_result: list[str] = balloon_festival.inspect_balloons(timestamp)
            print(f"InspectBalloons={inspect_result}")
        else:
            print(f"Malformed input! {keyword}", file=sys.stderr)
            sys.exit(-1)


if __name__ == "__main__":
    main()