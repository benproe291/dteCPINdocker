describe('formDataToData', () => {
  it('should convert formData to data object', () => {
    const formData = new FormData();
    formData.append('name', 'John Doe');
    formData.append('age', '30');

    const expectedData = {
      name: 'John Doe',
      age: '30',
    };

    const data = formDataToData(formData);
    expect(data).toEqual(expectedData);
  });

  it('should handle empty formData', () => {
    const formData = new FormData();

    const expectedData = {};

    const data = formDataToData(formData);
    expect(data).toEqual(expectedData);
  });

  it('should handle formData with multiple values for the same key', () => {
    const formData = new FormData();
    formData.append('name', 'John Doe');
    formData.append('name', 'Jane Smith');

    const expectedData = {
      name: ['John Doe', 'Jane Smith'],
    };

    const data = formDataToData(formData);
    expect(data).toEqual(expectedData);
  });
});