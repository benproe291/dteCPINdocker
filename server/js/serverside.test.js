describe('request', () => {
  it('should have the correct parent value', () => {
    const location = 'us-central1';
    const projectId = '606286572956';
    const endpointId = '2161545302207627264';
    const instances = ['instance1', 'instance2'];

    const expectedParent = `projects/${projectId}/locations/${location}/endpoints/${endpointId}`;

    const request = {
      parent: expectedParent,
      requestBody: {
        instances: instances
      }
    };

    expect(request.parent).toEqual(expectedParent);
  });

  it('should have the correct requestBody value', () => {
    const projectId = 'my-project';
    const location = 'us-central1';
    const endpointId = 'my-endpoint';
    const instances = ['instance1', 'instance2'];

    const expectedRequestBody = {
      instances: instances
    };

    const request = {
      parent: `projects/${projectId}/locations/${location}/endpoints/${endpointId}`,
      requestBody: expectedRequestBody
    };

    expect(request.requestBody).toEqual(expectedRequestBody);
  });
});