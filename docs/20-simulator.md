# 20. 시뮬레이터 개발

openpilot 테스트를 위한 시뮬레이터를 만듭니다.

## CARLA 연동

```python
import carla

class OpenpilotSimulator:
    def __init__(self):
        self.client = carla.Client('localhost', 2000)
        self.world = self.client.get_world()
        
        # 차량 생성
        bp = self.world.get_blueprint_library().find('vehicle.tesla.model3')
        self.vehicle = self.world.spawn_actor(bp, carla.Transform())
        
        # 카메라
        camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
        self.camera = self.world.spawn_actor(
            camera_bp,
            carla.Transform(carla.Location(x=1.5, z=2.4)),
            attach_to=self.vehicle
        )
    
    def step(self, steer, throttle):
        # 제어 적용
        control = carla.VehicleControl()
        control.steer = steer
        control.throttle = throttle
        self.vehicle.apply_control(control)
        
        # 센서 데이터 받기
        image = self.camera.get_data()
        
        return image
```

## openpilot 연결

```python
# 브릿지
from cereal import messaging

pm = messaging.PubMaster(['roadCameraState'])

while True:
    # CARLA 이미지
    image = simulator.get_camera_frame()
    
    # openpilot에 전송
    msg = messaging.new_message('roadCameraState')
    msg.roadCameraState.image = image
    pm.send('roadCameraState', msg)
```

---

[다음: 21. 프로덕션 배포 →](./21-deployment.md)
