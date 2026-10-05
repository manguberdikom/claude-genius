package shop.web;

/**
 * "Javadoc" ichida catch (Exception e) {} va e.printStackTrace() bor.
 */
public class Literals {

    private static final String BASE = "http://inventory";
    private static final String DOC = "do not call e.printStackTrace() here";
    private static final String TYPES = "image/*";
    private static final String API = "/api/**";
    private static final char QUOTE = '"';
    private static final char APOS = '\'';
    private static final String ESCAPED = "a \"quoted\" System.out.println()";
    private static final String TEMPLATE = """
        try { x(); } catch (Exception e) {}
        // "System.out.println" bu matn, kod emas
        """;

    public void quiet() {
        try {
            run(BASE + TYPES + API + QUOTE + APOS + ESCAPED + TEMPLATE + DOC);
        } catch (IllegalStateException e) {
        }
    }
}
