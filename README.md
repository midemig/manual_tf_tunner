# manual_tf_tunner

Simple node to adjust tf values between two frames manually

### How to run:

1. Manually set in python code the frames and the initial values of the tf (TODO: Set it as parameters)

2. Run node

```
ros2 run manual_tf_tunner manual_tf_tunner_node
```

3. Change the values. 

#### KEYS:

- **x**: Change X values 
- **y**: Change Y values 
- **z**: Change Z values 
- **r**: Change Roll values 
- **p**: Change Pitch values 
- **w**: Change Yaw values 
- **+**: Increment step amount the selected value
- **-**: Decrement step amount the selected value
- <b>*</b>: Multiply by 10 the step
- **/**: Divide by 10 the step
