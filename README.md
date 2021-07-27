This is core module of vsdkx.

In here all the interfaces needed for model drivers and addon are defined.

### EventDetector
You can add **one** model driver and **many** addons to your project, 
`EventDetector` will call all the addons' `pre_process` method and then calls 
the model driver's `inference` method on pre processed frame to receive the 
inference result and after that all the addons' `post_process` method will be 
called on the inference.    

### SimpleRunner
You can use SimpleRunner to run the application with cli commands or you can 
also start your application with gRPC server and send the frames via that. 
You can pass a method to SimpleRunner and with that on each frame you have 
access to the frame and the inference result and you can implement your own 
business with that

