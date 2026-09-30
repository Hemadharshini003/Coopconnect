import 'package:flutter_test/flutter_test.dart';
import 'package:coopconnect_mobile/main.dart';

void main() {
  testWidgets('CoopConnect App loads splash screen', (WidgetTester tester) async {
    await tester.pumpWidget(const CoopConnectApp());
    expect(find.text('CoopConnect AI'), findsOneWidget);
  });
}
